# Research Dossier: The Thinking Machines Connection Machine CM-2 (1987)

## 1. Technical Specifications (Massive Simplicity)
*   **Architecture:** SIMD (Single Instruction, Multiple Data).
*   **Processors:** Up to 65,536 (64K) individual 1-bit processors. Each processor handles one bit at a time, allowing for massive parallel operations on simple data types.
*   **Clock Speed:** ~7 MHz.
*   **Memory:** Up to 512 MB of total system RAM. Each processor has between 4 KB and 64 KB of local memory.
*   **Interconnect:** A **12-dimensional Boolean hypercube** network ($2^{12} = 4,096$ chips). Each chip contains 16 processors and a router chip that manages communication across the 12th-dimension vertices. Any two chips are at most 12 hops away.
*   **Floating Point:** Optional Weitek 3132 floating-point accelerators (one shared by every 32 processors). Peak performance of ~2.5 GigaFLOPS.
*   **I/O & Storage:** Supported the **DataVault**, a massive RAID disk system (up to 25 GB) that could stream data into the machine at high speeds, a first for its time.
*   **Software:** Controlled by a host "front-end" (Symbolics Lisp Machine, VAX, or Sun-4). Programmed in \*Lisp, C\*, and CM Fortran.

## 2. The Feynman Factor
*   **Router Buffer Optimization:** Richard Feynman, acting as a consultant, analyzed the traffic patterns in the 12D hypercube router. While engineers thought 7 buffers per chip were needed, Feynman used differential equations to prove that **5 buffers** were sufficient, allowing the design to fit on the silicon.
*   **Feynman’s Logarithm Algorithm:** He developed a high-precision, parallel algorithm for computing logarithms using bit-shifting and addition, optimized for 1-bit processors.
*   **QCD Calculations:** Feynman used the CM-2 to perform Quantum Chromodynamics (QCD) simulations, proving its superiority over specialized hardware.

## 3. Industrial Design: The "Cube of Cubes"
*   **Designer:** Tamiko Thiel (Lead Industrial Designer).
*   **Form:** A 5-foot (1.5m) cube composed of 8 smaller sub-cubes. The physical arrangement is a visual metaphor for the internal 12-dimensional hypercube topology.
*   **LEDs:** 4,096 red status LEDs (one for each 16-processor chip). The LEDs flicker to show processor activity, creating a "pulsing brain" effect.
*   **Aesthetics:** Black anodized aluminum and translucent Plexiglas, designed to make the act of "thinking" visible.

## 4. Modern AI Connection (GPU Ancestry)
*   **The SIMD Legacy:** Modern NVIDIA GPUs (CUDA/OpenCL) are essentially evolved SIMD machines. The CM-2's model of thousands of simple cores is the direct ancestor of modern GPU computing.
*   **Deep Learning Philosophy:** Founder Danny Hillis believed "intelligence emerges from connections," mirroring the current paradigm where complex behavior emerges from scaled, interconnected simple nodes (neurons).
*   **WAIS & Search:** Brewster Kahle used the CM-2 to build **WAIS** (Wide Area Information Servers), the first natural language search engine, which paved the way for modern search and the Internet Archive.

## 5. Cultural Significance
*   **Jurassic Park:** The CM-2 (and later CM-5) featured in the movie *Jurassic Park* as the park's control system.
*   **Scientific Impact:** Used for weather forecasting, fluid dynamics (Navier-Stokes), and seismic processing.

---
**Artifacts in Collection:**
- **Primary Image:** `images/CM2_animated.webp` (High-resolution animation of LED activity).
- **Secondary Image:** `images/CM2_DataVault_thumb.png` (Visual of the RAID storage system).
---
**Next Step:** Passing this research to the **Museum Outliner** to structure the **Niche "Spotlight" Article (Format 4)**.
