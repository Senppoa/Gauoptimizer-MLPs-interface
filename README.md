# MLPs calculator interface for Gaussian

This project provides a solution for integrating MLPs (MACE) models with Gaussian computational tasks. By offering both online and local operating modes, it aims to accelerate the calculation of energies and forces in molecular simulations, significantly improving computational efficiency.

## Features

*   **Model Persistent Online:** The model remains active on the server side, avoiding repeated loading for each calculation.
*   **In-Memory Data Transfer:** XYZ coordinate files are not saved locally but are directly uploaded to the server via memory, reducing disk I/O overhead.
*   **Session Persistence:** Application sessions remain active online, avoiding the overhead of repeatedly opening new sessions.
*   **Dual Mode Support:** Provides both an online version (suitable for network environments) and a local version (offering higher operational speed).

## Operating Modes

### 1. Online Version

The online version, as the first iteration, runs the online MACE model via Flask and keeps it persistent, returning calculated energies and forces. Please note that network speed might become a bottleneck for performance.

#### Usage

1.  **Activate Virtual Environment:**
    ```bash
    conda activate rmlp # Or your preferred virtual environment manager
    ```
2.  **Start the Online Server:**
    ```bash
    python server.py
    ```
3.  **Run Gaussian Calculation Task:**
    In another command line window, start your Gaussian calculation task. In the Gaussian GJF input file, you will need to configure it to call the `runner.py` script to interact with the online server.

### 2. Local Version

The local version employs a dual-threaded operation, providing faster execution speeds compared to the online version.

#### Usage

1.  **Activate Virtual Environment:**
    ```bash
    conda activate rmlp # Or your preferred virtual environment manager
    ```
2.  **Start the Local Application Server (Gunicorn):**
    Use Gunicorn to start the local Flask application. Ensure that the `/home/tangkun/tmp` path exists and has read/write permissions, or replace it with your custom path.
    ```bash
    gunicorn --bind unix:/home/tangkun/tmp/flask_server.sock server:app
    ```
3.  **Run Gaussian Calculation Task:**
    In another command line window, start your Gaussian calculation task. In the Gaussian GJF input file, you will need to configure it to call the `runner.py` script to interact with the local server.

## Dependencies

To ensure the proper functioning of the project, especially the local version, please install the following dependencies:

*   **rmlp Virtual Environment:** All operations must be performed within an activated `rmlp` virtual environment (or other corresponding environment).
*   **requests_unixsocket2:** **For the local version, this is a mandatory dependency. Please ensure you install the specified version.**
    ```bash
    pip install requests_unixsocket2==0.4.1
    ```

## Performance Acceleration Principles

The speed improvements of this project primarily stem from the following optimizations:

1.  **Model Persistent Online:** The MACE/RMLP model continuously runs on the server side, eliminating the need to reload it for each calculation.
2.  **In-Memory XYZ Coordinate File Transfer:** This avoids the process of writing XYZ coordinate data to disk and then reading it back, instead performing direct data transfer via memory.
3.  **Application Session Persistence:** Maintains long-lived application sessions, reducing the overhead of repeatedly establishing and closing sessions.

Building upon these optimizations, the local version further enhances speed by utilizing local IPC (Inter-Process Communication) instead of network communication, thereby reducing potential network latency and achieving a slight additional speed boost.