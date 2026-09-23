# Avian 3D Acoustic Point Cloud & Vocal Frequency Visualizer

An interactive 3D acoustic visualization suite for exploring avian vocal dynamics, voice frequency modulations, tone trajectories, and acoustic niches across 20 bird species from the **Western Mediterranean Wetlands Bird Dataset** ([Zenodo 7505820](https://zenodo.org/records/7505820)).

---

## 🌟 Highlights & Features

- **3D Acoustic Point Cloud**:
  - Off-white canvas aesthetic matching modern scientific visualization standards:
    - **$X$-axis**: Time (0 to 12.0 seconds)
    - **$Y$-axis**: Frequency (0 to 8,000 Hz)
    - **$Z$-axis**: Acoustic Vocal Energy ($-60$ to $-10$ dB)
  - Point opacity encodes pitch confidence and loudness (*"dimmer points are less certain"*).
- **Dynamic 3D Tone Tracking (Ascent & Descent)**:
  - Active 3D beacons dynamically climb **UP** along the frequency axis when tone/pitch rises ($\nearrow$) and slide **DOWN** when pitch drops ($\searrow$), leaving a trailing motion ribbon.
- **Bird Photographs Directly Alongside the 3D Plot**:
  - High-resolution photographs cached locally for each species displayed adjacent to the 3D canvas.
  - Automatically updates with species common name, Latin scientific name, acoustic role, frequency operating range, and habitat bio.
- **12+ Second Continuous Audio Playback**:
  - Full-length vocalization sequences extracted from Zenodo recordings.
  - Play, pause, scrub, and speed-rate control (**0.5x Slow-Motion**, **0.75x**, **1.0x Normal**).
- **Tone & Note Syllable Segmentation**:
  - Automatic note onset/offset detection and tone classification (*Rising Whistle*, *Falling Slur*, *Trill/Warble*, *Steady Tone*).
  - Click any detected note to immediately jump playback and watch the 3D point track the acoustic inflection.
- **Zero Full-Archive Download Ingestion**:
  - Utilizes HTTP Range extraction directly against Zenodo's multi-gigabyte zip archives (`spectrograms.zip` and `audio_files.zip`) to pull exact audio slices and spectrogram frames in seconds.

---

## 🦅 Species Included (20 Mediterranean Wetland Species)

| Scientific Name | Common Name | Acoustic Category | Dominant Frequency |
|---|---|---|---|
| *Acrocephalus arundinaceus* | Great Reed Warbler | Complex Melodic Song | 1.5 – 6.5 kHz |
| *Alcedo atthis* | Common Kingfisher | Piercing Whistle | 4.0 – 8.5 kHz |
| *Botaurus stellaris* | Great Bittern | Deep Bass Boom | 0.15 – 0.9 kHz |
| *Himantopus himantopus* | Black-winged Stilt | Staccato Yapping | 1.8 – 5.5 kHz |
| *Dendrocopos minor* | Lesser Spotted Woodpecker | Harmonic Piping | 3.0 – 7.5 kHz |
| *Tachybaptus ruficollis* | Little Grebe | Whinnying Trill | 1.8 – 5.8 kHz |
| *Motacilla flava* | Western Yellow Wagtail | Slurred Flight Whistle | 3.5 – 7.5 kHz |
| *Anas platyrhynchos* | Mallard | Descending Harmonic Quack | 0.6 – 2.8 kHz |
| *Fulica atra* | Eurasian Coot | Metallic Chip | 1.2 – 4.5 kHz |
| *Porphyrio porphyrio* | Western Swamphen | Trumpeting Honk | 0.8 – 3.8 kHz |
| *Ciconia ciconia* | White Stork | Bill-Clattering | 0.5 – 4.5 kHz |
| *Circus aeruginosus* | Western Marsh Harrier | High Raptor Yelp | 2.0 – 5.5 kHz |
| *Coracias garrulus* | European Roller | Rolling Rasp | 1.0 – 3.8 kHz |
| *Ixobrychus minutus* | Little Bittern | Barking Croak | 0.4 – 2.0 kHz |
| *Charadrius alexandrinus* | Kentish Plover | Soft Piping | 1.5 – 4.5 kHz |
| *Acrocephalus scirpaceus* | Eurasian Reed Warbler | Rhythmic Churring | 2.0 – 6.5 kHz |
| *Acrocephalus melanopogon* | Moustached Warbler | Sweet Warble | 2.0 – 6.0 kHz |
| *Anas strepera* | Gadwall | Reed Grunt | 0.8 – 3.2 kHz |
| *Gallinula chloropus* | Common Moorhen | Guttural Squawk | 1.0 – 4.2 kHz |
| *Ardea purpurea* | Purple Heron | Guttural Croak | 0.5 – 2.5 kHz |

---

## 🚀 Getting Started

### 1. Run Local Visualizer
```bash
python serve_visualizer.py
```
Or start Python's built-in HTTP server:
```bash
python -m http.server 8080
```
Open **`http://localhost:8080/visualizer.html`** in your browser.

### 2. Standalone Plotly Visualizations
Open any of the standalone Plotly 3D HTML models directly in any browser:
- `point_cloud_3d.html`: 3D Point Cloud multi-species view.
- `multi_species_comparison_3d.html`: Multi-species comparison.
- `warbler_surface_3d.html`, `kingfisher_surface_3d.html`, `bittern_surface_3d.html`: Individual 3D acoustic surfaces.

---

## 📂 Repository Structure

```
├── audio/                          # 12s continuous MP3 audio clips for bird species
├── data/
│   ├── bird_vocalizations_12s.json # Continuous 12s STFT, notes, and tone slopes
│   ├── bird_vocalizations.json     # 1-second Mel-spectrogram datasets
│   └── metadata.csv                # Dataset metadata from Zenodo 7505820
├── images/                         # High-resolution photographs of all 20 species
├── visualizer.html                 # Main interactive 3D web application
├── point_cloud_3d.html             # Standalone 3D point cloud plot
├── serve_visualizer.py             # Simple web server launcher
├── prepare_12s_vocalizations.py    # Pipeline for audio slicing, STFT & note detection
├── fetch_and_prepare_dataset.py    # HTTP Range archive ingestion script
└── generate_3d_plots.py            # Plotly 3D generation script
```

---

## 📜 Dataset Citation
Dataset sourced from:
> *Western Mediterranean Wetlands Bird Dataset*, Zenodo Records 7505820.  
> DOI: [10.5281/zenodo.7505820](https://doi.org/10.5281/zenodo.7505820)
