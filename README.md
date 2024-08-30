# RugbyRefQuiz
Personal tool to test rugby refereeing knowledge

---

## Setting Up the Environment

1. **Create the Conda Environment:**
   Open your WSL terminal, navigate to the directory containing the `environment.yml` file, and run the following command:
   ```bash
   conda env create -f environment.yml
   ```

2. **Activate the Environment:**
   After the environment is created, activate it using:
   ```bash
   conda activate RefQuiz
   ```

3. **Installing tkinter:**
    Remember to install tkinter as it is not included in the `requirements.txt` file.
    For conda:
       ```bash
    conda install tk
   ```
   For Ubuntu/Debian:
   ```bash
    sudo apt-get install python3-tk
   ```
---
