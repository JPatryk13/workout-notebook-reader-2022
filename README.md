# Workout Notebook Reader
Small pipeline reading `.txt` files with my workout info, filtering out (inconsistent) notation style and writing data to `.JSON` files for future analysis.
## Set-up
1. Clone repository `$ git clone https://github.com/jpatryk7/workout_notebook_reader.git`.
2. Create a new virtual environment in the project directory`$ cd workout_notebook_reader`, `$ python -m venv venv`.
3. When using IDE configure it to use the newly added virtual environment or activate it from the terminal. Before proceeding make sure that `(venv)` is displayed to the left of a new line.
4. Install required packages `(venv) $ pip install -r requirements.txt`.
5. If running first time ensure that the `output/workouts/` directory is empty. Ensure that the appropriate `.txt` file with workout notes is supplied in `input/`.
6. From the directory `workout_notebook_reader` run `(venv) $ python read.py --filename file_with_workout_notes.txt`. The output should appear in `output/workouts/`. If using the default file provided run `(venv) $ python read.py --filename initial_21102022.txt`.
