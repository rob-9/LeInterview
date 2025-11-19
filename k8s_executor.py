"""
Kubernetes Job Executor for Code Execution
Handles creating and managing Kubernetes Jobs for secure code execution
"""
import time
import uuid
import yaml
from kubernetes import client, config
from kubernetes.client.rest import ApiException


class KubernetesCodeExecutor:
    """Manages code execution via Kubernetes Jobs"""

    def __init__(self, namespace='interview-platform'):
        """Initialize Kubernetes client"""
        self.namespace = namespace
        try:
            # Try in-cluster config first (when running in K8s)
            config.load_incluster_config()
        except config.ConfigException:
            # Fall back to kubeconfig (for local development)
            config.load_kube_config()

        self.batch_v1 = client.BatchV1Api()
        self.core_v1 = client.CoreV1Api()

    def _load_job_template(self, language):
        """Load the appropriate job template for the language"""
        template_map = {
            'python': 'k8s/code-runners/python-runner.yaml',
            'java': 'k8s/code-runners/java-runner.yaml',
            'c++': 'k8s/code-runners/cpp-runner.yaml'
        }

        template_path = template_map.get(language)
        if not template_path:
            raise ValueError(f"Unsupported language: {language}")

        with open(template_path, 'r') as f:
            return yaml.safe_load(f)

    def _create_job_from_template(self, language, code, job_id):
        """Create a Job object from template with code injected"""
        job_template = self._load_job_template(language)

        # Replace placeholders
        job_name = f"{language}-executor-{job_id}"
        job_template['metadata']['name'] = job_name

        # Inject code into the job spec
        container = job_template['spec']['template']['spec']['containers'][0]

        if language == 'python':
            # For Python, replace the args with the actual code
            container['args'] = [code]
        else:
            # For Java and C++, replace CODE_PLACEHOLDER in the command
            command_str = container['args'][0]
            container['args'][0] = command_str.replace('CODE_PLACEHOLDER', code)

        return job_template, job_name

    def execute_code(self, code, language='python', timeout=30):
        """
        Execute code in a Kubernetes Job

        Args:
            code: The code to execute
            language: Programming language (python, java, c++)
            timeout: Maximum execution time in seconds

        Returns:
            dict: {'output': str, 'error': str, 'status': str}
        """
        job_id = str(uuid.uuid4())[:8]

        try:
            # Create job from template
            job_manifest, job_name = self._create_job_from_template(
                language, code, job_id
            )

            # Create the job
            self.batch_v1.create_namespaced_job(
                namespace=self.namespace,
                body=job_manifest
            )

            # Wait for job completion
            result = self._wait_for_job_completion(job_name, timeout)

            # Get pod logs
            output = self._get_job_logs(job_name)

            # Cleanup job
            self._delete_job(job_name)

            return {
                'output': output,
                'error': '' if result == 'succeeded' else 'Job failed',
                'status': result
            }

        except ApiException as e:
            return {
                'output': '',
                'error': f"Kubernetes API error: {e.reason}",
                'status': 'failed'
            }
        except Exception as e:
            return {
                'output': '',
                'error': str(e),
                'status': 'failed'
            }

    def _wait_for_job_completion(self, job_name, timeout):
        """Wait for job to complete or timeout"""
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                job = self.batch_v1.read_namespaced_job_status(
                    name=job_name,
                    namespace=self.namespace
                )

                # Check if job succeeded
                if job.status.succeeded:
                    return 'succeeded'

                # Check if job failed
                if job.status.failed:
                    return 'failed'

                # Still running, wait a bit
                time.sleep(0.5)

            except ApiException as e:
                if e.status == 404:
                    return 'not_found'
                raise

        # Timeout reached
        return 'timeout'

    def _get_job_logs(self, job_name):
        """Get logs from the job's pod"""
        try:
            # Find pods for this job
            pods = self.core_v1.list_namespaced_pod(
                namespace=self.namespace,
                label_selector=f"job-name={job_name}"
            )

            if not pods.items:
                return "No pods found for job"

            # Get logs from the first pod
            pod_name = pods.items[0].metadata.name
            logs = self.core_v1.read_namespaced_pod_log(
                name=pod_name,
                namespace=self.namespace,
                container=pods.items[0].spec.containers[0].name
            )

            return logs

        except ApiException as e:
            return f"Error getting logs: {e.reason}"

    def _delete_job(self, job_name):
        """Delete a job and its pods"""
        try:
            # Delete job (propagation policy will delete pods too)
            self.batch_v1.delete_namespaced_job(
                name=job_name,
                namespace=self.namespace,
                propagation_policy='Foreground'
            )
        except ApiException:
            pass  # Ignore deletion errors

    def get_active_jobs(self):
        """Get count of active code execution jobs"""
        try:
            jobs = self.batch_v1.list_namespaced_job(
                namespace=self.namespace,
                label_selector="role=code-executor"
            )
            return len([j for j in jobs.items if j.status.active])
        except ApiException:
            return 0

    def cleanup_old_jobs(self, max_age_seconds=300):
        """Clean up jobs older than max_age_seconds"""
        try:
            jobs = self.batch_v1.list_namespaced_job(
                namespace=self.namespace,
                label_selector="role=code-executor"
            )

            current_time = time.time()
            for job in jobs.items:
                job_age = current_time - job.metadata.creation_timestamp.timestamp()
                if job_age > max_age_seconds:
                    self._delete_job(job.metadata.name)

        except ApiException:
            pass  # Ignore errors during cleanup
