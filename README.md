[index.html](https://github.com/user-attachments/files/23109422/index.html)
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <meta http-equiv="Content-Style-Type" content="text/css">
  <title></title>
  <meta name="Generator" content="Cocoa HTML Writer">
  <meta name="CocoaVersion" content="1894.7">
  <style type="text/css">
    p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; font: 12.0px Helvetica; color: #000000; -webkit-text-stroke: #000000}
    p.p2 {margin: 0.0px 0.0px 0.0px 0.0px; font: 12.0px Helvetica; color: #000000; -webkit-text-stroke: #000000; min-height: 14.0px}
    span.s1 {font-kerning: none}
  </style>
</head>
<body>
<p class="p1"><span class="s1">&lt;!DOCTYPE html&gt;</span></p>
<p class="p1"><span class="s1">&lt;html lang="es" class="h-full bg-gray-900"&gt;</span></p>
<p class="p1"><span class="s1">&lt;head&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>&lt;meta charset="UTF-8"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>&lt;meta name="viewport" content="width=device-width, initial-scale=1.0"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>&lt;title&gt;Oráculo de Causalidad Global&lt;/title&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>&lt;!-- Carga de Tailwind CSS --&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>&lt;script src="https://cdn.tailwindcss.com"&gt;&lt;/script&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>&lt;style&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>/* Estilo personalizado para el scrollbar en el panel de resultados */</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>#results-panel::-webkit-scrollbar {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>width: 8px;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>#results-panel::-webkit-scrollbar-track {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>background: #1f2937; /* bg-gray-800 */</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>#results-panel::-webkit-scrollbar-thumb {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>background: #4b5563; /* bg-gray-600 */</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>border-radius: 4px;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>#results-panel::-webkit-scrollbar-thumb:hover {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>background: #6b7280; /* bg-gray-500 */</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>/* Estilo para el loader */</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>.loader {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>border-top-color: #3498db;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>animation: spin 1s linear infinite;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>@keyframes spin {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>to { transform: rotate(360deg); }</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>&lt;/style&gt;</span></p>
<p class="p1"><span class="s1">&lt;/head&gt;</span></p>
<p class="p1"><span class="s1">&lt;body class="h-full text-white overflow-hidden"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>&lt;div class="flex h-screen"&gt;</span></p>
<p class="p2"><span class="s1"><span class="Apple-converted-space">        </span></span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>&lt;!-- Panel Izquierdo: Consulta y Capas --&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>&lt;div class="w-full lg:w-1/3 xl:w-1/4 p-6 bg-gray-900 bg-opacity-80 flex flex-col backdrop-blur-sm shadow-2xl z-10 overflow-y-auto"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>&lt;h1 class="text-2xl font-bold text-blue-300 mb-4"&gt;Oráculo de Causalidad&lt;/h1&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>&lt;p class="text-sm text-gray-400 mb-6"&gt;Módulos de simulación y visualización.&lt;/p&gt;</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>&lt;!-- Módulo 3: Consola de Consulta --&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>&lt;div class="mb-6"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>&lt;h2 class="text-lg font-semibold text-gray-200 mb-3"&gt;Consola de Consulta (Input)&lt;/h2&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>&lt;label for="scenario-input" class="block text-sm font-medium text-gray-400 mb-2"&gt;Plantea un escenario "What If...":&lt;/label&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>&lt;textarea id="scenario-input" rows="6" class="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg shadow-inner focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-200 resize-none" placeholder="Ej: ¿Qué pasaría si se descubre una forma de desalinización 90% más barata?"&gt;&lt;/textarea&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>&lt;button id="run-simulation" class="mt-4 w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg transition duration-300 ease-in-out transform hover:scale-105"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>Ejecutar Simulación</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>&lt;/button&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>&lt;/div&gt;</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>&lt;!-- Módulo 1: Capas de Datos (Mockup) --&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>&lt;div&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>&lt;h2 class="text-lg font-semibold text-gray-200 mb-3"&gt;Atlas de Datos Vivos (Capas)&lt;/h2&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>&lt;div class="space-y-3"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>&lt;label class="flex items-center text-gray-300"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>&lt;input type="checkbox" data-layer="population" class="form-checkbox bg-gray-700 border-gray-600 text-blue-500 rounded focus:ring-blue-500"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>&lt;span class="ml-3"&gt;Densidad de Población&lt;/span&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>&lt;/label&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>&lt;label class="flex items-center text-gray-300"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>&lt;input type="checkbox" data-layer="laws" class="form-checkbox bg-gray-700 border-gray-600 text-blue-500 rounded focus:ring-blue-500"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>&lt;span class="ml-3"&gt;Corpus Legislativo (Tipo X)&lt;/span&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>&lt;/label&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>&lt;label class="flex items-center text-gray-300"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>&lt;input type="checkbox" data-layer="trade" class="form-checkbox bg-gray-700 border-gray-600 text-blue-500 rounded focus:ring-blue-500"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>&lt;span class="ml-3"&gt;Rutas Comerciales Globales&lt;/span&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>&lt;/label&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>&lt;label class="flex items-center text-gray-300"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>&lt;input type="checkbox" data-layer="climate" class="form-checkbox bg-gray-700 border-gray-600 text-blue-500 rounded focus:ring-blue-500"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>&lt;span class="ml-3"&gt;Anomalías Climáticas&lt;/span&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>&lt;/label&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>&lt;/div&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>&lt;/div&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>&lt;/div&gt;</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>&lt;!-- Panel Central: Globo 3D --&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>&lt;div id="globe-container" class="flex-1 h-full relative z-0"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>&lt;!-- El canvas de Three.js se insertará aquí --&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>&lt;/div&gt;</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>&lt;!-- Panel Derecho: Resultados --&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>&lt;div class="w-full lg:w-1/3 xl:w-2/5 p-6 bg-gray-900 bg-opacity-80 flex flex-col backdrop-blur-sm shadow-2xl z-10"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>&lt;h2 class="text-lg font-semibold text-gray-200 mb-3"&gt;Panel de Resultados (Output)&lt;/h2&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>&lt;div id="results-panel" class="flex-1 bg-gray-800 border border-gray-700 rounded-lg shadow-inner p-4 overflow-y-auto"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>&lt;div id="loader" class="hidden items-center justify-center h-full"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>&lt;div class="loader ease-linear rounded-full border-4 border-t-4 border-gray-600 h-12 w-12 mb-4"&gt;&lt;/div&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>&lt;p class="text-gray-400"&gt;Calculando árbol de probabilidades...&lt;/p&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>&lt;/div&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>&lt;div id="results-content" class="text-gray-300 prose prose-invert prose-sm"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>&lt;p class="text-gray-500"&gt;Los resultados de la simulación aparecerán aquí.&lt;/p&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>&lt;/div&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>&lt;/div&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>&lt;/div&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>&lt;/div&gt;</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>&lt;!-- Carga de Three.js (como módulo) --&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>&lt;script type="importmap"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>{</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>"imports": {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>"three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>"three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>&lt;/script&gt;</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>&lt;script type="module"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>import * as THREE from 'three';</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>import { OrbitControls } from 'three/addons/controls/OrbitControls.js';</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>let scene, camera, renderer, globe, controls;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>let globeMaterial;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>const globeContainer = document.getElementById('globe-container');</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>// --- MÓDULO 3: GLOBO INTERACTIVO ---</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>function initGlobe() {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>// Escena</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>scene = new THREE.Scene();</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>scene.background = new THREE.Color(0x050a14); // Fondo oscuro casi negro</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>// Cámara</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>camera = new THREE.PerspectiveCamera(75, globeContainer.clientWidth / globeContainer.clientHeight, 0.1, 1000);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>camera.position.z = 15;</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>// Renderer</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>renderer = new THREE.WebGLRenderer({ antialias: true });</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>renderer.setSize(globeContainer.clientWidth, globeContainer.clientHeight);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>globeContainer.appendChild(renderer.domElement);</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>// Luces</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>const ambientLight = new THREE.AmbientLight(0x404040, 2); // Luz ambiental suave</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>scene.add(ambientLight);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>const directionalLight = new THREE.DirectionalLight(0xffffff, 1);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>directionalLight.position.set(5, 3, 5);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>scene.add(directionalLight);</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>// Creación del Globo (Representación de datos)</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>const geometry = new THREE.SphereGeometry(7, 64, 64);</span></p>
<p class="p2"><span class="s1"><span class="Apple-converted-space">            </span></span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>// Usamos un material que parece "tecnológico" o de "datos"</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>globeMaterial = new THREE.MeshPhongMaterial({</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>color: 0x0077be, // Azul base</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>wireframe: true, // Mostrar como malla de alambre</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>shininess: 50</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>});</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>globe = new THREE.Mesh(geometry, globeMaterial);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>scene.add(globe);</span></p>
<p class="p2"><span class="s1"><span class="Apple-converted-space">            </span></span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>// Añadir una "atmósfera" sutil</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>const atmosphereGeometry = new THREE.SphereGeometry(7.2, 64, 64);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>const atmosphereMaterial = new THREE.ShaderMaterial({</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>vertexShader: `</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>varying vec3 vNormal;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>void main() {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>vNormal = normalize(normalMatrix * normal);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>`,</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>fragmentShader: `</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>varying vec3 vNormal;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>void main() {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>float intensity = pow(0.6 - dot(vNormal, vec3(0.0, 0.0, 1.0)), 4.0);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>gl_FragColor = vec4(0.3, 0.6, 1.0, 1.0) * intensity;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>`,</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>blending: THREE.AdditiveBlending,</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>side: THREE.BackSide,</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>transparent: true</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>});</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>const atmosphere = new THREE.Mesh(atmosphereGeometry, atmosphereMaterial);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>scene.add(atmosphere);</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>// Controles de órbita (para rotar el globo)</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>controls = new OrbitControls(camera, renderer.domElement);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>controls.enableDamping = true;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>controls.dampingFactor = 0.05;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>controls.minDistance = 10;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>controls.maxDistance = 50;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>controls.enablePan = false; // Deshabilitar paneo</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>// Manejador de redimensionamiento de ventana</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>window.addEventListener('resize', onWindowResize, false);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>}</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>function animate() {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>requestAnimationFrame(animate);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>globe.rotation.y += 0.0005; // Rotación lenta y constante</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>controls.update();</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>renderer.render(scene, camera);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>}</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>function onWindowResize() {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>if (!globeContainer) return;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>camera.aspect = globeContainer.clientWidth / globeContainer.clientHeight;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>camera.updateProjectionMatrix();</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>renderer.setSize(globeContainer.clientWidth, globeContainer.clientHeight);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>}</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>// --- Lógica de Capas (Mockup) ---</span></p>
<p class="p2"><span class="s1"><span class="Apple-converted-space">        </span></span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>const layerCheckboxes = document.querySelectorAll('input[data-layer]');</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>const baseColor = new THREE.Color(0x0077be);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>const layerColors = {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>population: new THREE.Color(0xff4500), // Naranja/Rojo</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>laws: new THREE.Color(0xeeee00), <span class="Apple-converted-space">      </span>// Amarillo</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>trade: new THREE.Color(0x00ff7f), <span class="Apple-converted-space">      </span>// Verde primavera</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>climate: new THREE.Color(0xffffff) <span class="Apple-converted-space">      </span>// Blanco</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>};</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>layerCheckboxes.forEach(checkbox =&gt; {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>checkbox.addEventListener('change', () =&gt; {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>let finalColor = new THREE.Color(0x000000); // Empezar en negro</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>let activeLayers = 0;</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>layerCheckboxes.forEach(cb =&gt; {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>if (cb.checked) {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>finalColor.add(layerColors[cb.dataset.layer]);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>activeLayers++;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>});</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>if (activeLayers === 0) {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>globeMaterial.color.set(baseColor);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>} else {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>// Promediar los colores si hay múltiples capas</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>finalColor.r /= activeLayers;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>finalColor.g /= activeLayers;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>finalColor.b /= activeLayers;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>globeMaterial.color.set(finalColor);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>});</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>});</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>// --- MÓDULO 2: SIMULACIÓN DE ORÁCULO (vía API de Gemini) ---</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>const runButton = document.getElementById('run-simulation');</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>const scenarioInput = document.getElementById('scenario-input');</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>const resultsContent = document.getElementById('results-content');</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>const loader = document.getElementById('loader');</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>const resultsPanel = document.getElementById('results-panel');</span></p>
<p class="p2"><span class="s1"><span class="Apple-converted-space">        </span></span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>const apiKey = ""; // La API key se inyectará en el entorno de ejecución</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`;</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>// El "cerebro" de la IA: define su personalidad y formato de respuesta</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>const SYSTEM_PROMPT = `</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>Eres el "Oráculo de Causalidad", el núcleo de IA de un sistema de simulación planetaria.</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>Tu propósito es analizar escenarios hipotéticos ("What If") y predecir las consecuencias en cascada (efecto mariposa).</span></p>
<p class="p2"><span class="s1"><span class="Apple-converted-space">            </span></span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>Un usuario ha introducido un escenario. Tu tarea es analizarlo basándote en patrones históricos, económicos, sociales y ambientales complejos.</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>REGLAS ESTRICTAS DE RESPUESTA:</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>1.<span class="Apple-converted-space">  </span>**NUNCA des una respuesta única y certera.** Tu respuesta DEBE ser un "árbol de probabilidades" detallado.</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>2.<span class="Apple-converted-space">  </span>**Proyecta consecuencias de 1er, 2do y N-ésimo orden.** Muestra cómo un evento se ramifica.</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>3.<span class="Apple-converted-space">  </span>**Usa porcentajes de probabilidad aproximados** (ej. "70% de probabilidad", "baja probabilidad", "alta probabilidad").</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>4.<span class="Apple-converted-space">  </span>**Cubre múltiples sectores:** ¿Cómo impacta esto en la economía, la sociedad, la política, el medio ambiente, la tecnología?</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>5.<span class="Apple-converted-space">  </span>**Formatea la respuesta** usando Markdown (listas anidadas) para que sea fácil de leer como un árbol de ramificaciones.</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>6.<span class="Apple-converted-space">  </span>Habla con autoridad, pero siempre en términos de probabilidad, no de certeza.</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>`;</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>runButton.addEventListener('click', handleSimulation);</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>async function handleSimulation() {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>const userQuery = scenarioInput.value;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>if (!userQuery.trim()) {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>resultsContent.innerHTML = '&lt;p class="text-yellow-400"&gt;Por favor, introduce un escenario válido.&lt;/p&gt;';</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>return;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>}</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>// Mostrar loader y ocultar contenido anterior</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>loader.style.display = 'flex';</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>resultsContent.style.display = 'none';</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>resultsPanel.scrollTop = 0; // Volver al inicio</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>runButton.disabled = true;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>runButton.textContent = 'Calculando...';</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>try {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>const responseText = await callGeminiAPI(userQuery);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>// Formatear respuesta (simple reemplazo de nueva línea por &lt;br&gt; para HTML)</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>const formattedResponse = responseText</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>.replace(/\n/g, '&lt;br&gt;')</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>.replace(/\*\*(.*?)\*\*/g, '&lt;strong&gt;$1&lt;/strong&gt;') // Negrita</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>.replace(/\*(.*?)\*/g, '&lt;em&gt;$1&lt;/em&gt;'); // Cursiva</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>resultsContent.innerHTML = formattedResponse;</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>} catch (error) {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>console.error("Error en la simulación:", error);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>resultsContent.innerHTML = `&lt;p class="text-red-400"&gt;Error al contactar al Oráculo de Causalidad. Por favor, inténtalo de nuevo.&lt;br&gt;&lt;br&gt;${error.message}&lt;/p&gt;`;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>} finally {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>// Ocultar loader y mostrar contenido</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>loader.style.display = 'none';</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>resultsContent.style.display = 'block';</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>runButton.disabled = false;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>runButton.textContent = 'Ejecutar Simulación';</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>}</span></p>
<p class="p2"><span class="s1"><span class="Apple-converted-space">        </span></span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>/**</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">         </span>* Llama a la API de Gemini con reintentos (exponential backoff)</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">         </span>* @param {string} userQuery - La consulta del usuario.</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">         </span>* @returns {Promise&lt;string&gt;} - El texto de respuesta del modelo.</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">         </span>*/</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>async function callGeminiAPI(userQuery) {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>const payload = {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>contents: [{<span class="Apple-converted-space"> </span></span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>parts: [{ text: userQuery }]<span class="Apple-converted-space"> </span></span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>}],</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>systemInstruction: {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>parts: [{ text: SYSTEM_PROMPT }]</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>},</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>generationConfig: {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>temperature: 0.7,</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>maxOutputTokens: 2048,</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>};</span></p>
<p class="p2"><span class="s1"><span class="Apple-converted-space">            </span></span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>let attempts = 0;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>const maxAttempts = 5;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>let delay = 1000; // 1 segundo</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>while (attempts &lt; maxAttempts) {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>try {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>const response = await fetch(apiUrl, {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>method: 'POST',</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>headers: { 'Content-Type': 'application/json' },</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>body: JSON.stringify(payload)</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>});</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>if (!response.ok) {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>const errorBody = await response.json();</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>throw new Error(`Error de API: ${response.status} ${response.statusText}. Detalles: ${JSON.stringify(errorBody.error)}`);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>}</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>const result = await response.json();</span></p>
<p class="p2"><span class="s1"><span class="Apple-converted-space">                    </span></span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>if (result.candidates &amp;&amp; result.candidates.length &gt; 0 &amp;&amp;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>result.candidates[0].content &amp;&amp; result.candidates[0].content.parts &amp;&amp;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>result.candidates[0].content.parts.length &gt; 0) {</span></p>
<p class="p2"><span class="s1"><span class="Apple-converted-space">                        </span></span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>return result.candidates[0].content.parts[0].text;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>} else {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>// Manejo de respuesta válida pero sin contenido (ej. filtro de seguridad)</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>if (result.promptFeedback) {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                            </span>console.warn("La respuesta fue bloqueada:", result.promptFeedback);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                            </span>throw new Error(`La simulación fue bloqueada por filtros de seguridad. Razón: ${result.promptFeedback.blockReason}`);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>throw new Error("Respuesta inesperada del Oráculo. Faltan datos.");</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>}</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>} catch (error) {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>attempts++;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>if (attempts &gt;= maxAttempts) {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>throw error; // Lanzar el error después de todos los intentos</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>console.warn(`Intento ${attempts} fallido. Reintentando en ${delay}ms...`);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>await new Promise(resolve =&gt; setTimeout(resolve, delay));</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>delay *= 2; // Duplicar el tiempo de espera</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>throw new Error("Se superaron todos los intentos de reintento de la API.");</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>}</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><br>
</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>// Iniciar la aplicación</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>initGlobe();</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>animate();</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>&lt;/script&gt;</span></p>
<p class="p1"><span class="s1">&lt;/body&gt;</span></p>
<p class="p1"><span class="s1">&lt;/html&gt;</span></p>
</body>
</html>
