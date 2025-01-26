import * as THREE from "https://cdn.skypack.dev/three@0.129.0/build/three.module.js";
import { OrbitControls } from "https://cdn.skypack.dev/three@0.129.0/examples/jsm/controls/OrbitControls.js";
import { GLTFLoader } from "https://cdn.skypack.dev/three@0.129.0/examples/jsm/loaders/GLTFLoader.js";

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 1, 5);

const renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById("container3D").appendChild(renderer.domElement);

// Add lights
const ambientLight = new THREE.AmbientLight(0x404040);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(1, 1, 1).normalize();
scene.add(directionalLight);

// Load the GLTF model
const loader = new GLTFLoader();
let model;

loader.load(
    '/looney_tunes_world_of_mayhem_le_bron_james/scene.gltf',
    (gltf) => {
        model = gltf.scene;
        scene.add(model);
        console.log("Model loaded successfully!");

        // Scale and center the model
        model.scale.set(3, 3, 3);
        const box = new THREE.Box3().setFromObject(model);
        const center = new THREE.Vector3();
        box.getCenter(center);
        model.position.sub(center);
    },
    undefined,
    (error) => {
        console.error("Error loading model:", error);
    }
);

// Add OrbitControls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.minDistance = 2;
controls.maxDistance = 10;

// Animation loop
function animate() {
    requestAnimationFrame(animate);
    controls.update(); // Required for damping
    renderer.render(scene, camera);
}
animate();

// Handle window resize
window.addEventListener("resize", () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// Typewriter Effect for Title and Subtitle
const title = document.getElementById("title");
const subtitle = document.getElementById("subtitle");

// Function to simulate typing
function typeWriter(element, text, speed, delay = 0) {
    setTimeout(() => {
        let i = 0;
        element.textContent = ""; // Clear any existing text
        const interval = setInterval(() => {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
            } else {
                clearInterval(interval);
                // Remove the cursor after typing is complete
                element.style.animation = "none"; // Stop the cursor animation
                element.style.borderRight = "none"; // Remove the cursor
            }
        }, speed);
    }, delay);
}

// Start typing animations
typeWriter(title, "LeInterview", 100); // Type title at 100ms per character
typeWriter(subtitle, "How can LeBron help you?", 50, 2000); // Type subtitle after 2 seconds