:: ---------------------------------------------
:: Add Environmental Variable for ffmpeg video encoder
:: This ensures ffmpeg is available system-wide
:: ---------------------------------------------
setx Path "%cd%\weights\ffmpeg-6.0-full_build\bin;%Path%"
REM setx Path "C:\B-Star\weights\ffmpeg-6.0-full_build\bin;%Path%"

:: ---------------------------------------------
:: Check if the Conda Environment directory exists
:: If it exists, skip creating the environment
:: ---------------------------------------------
if exist .\venvpy_3.9 (
    echo Conda environment already exists.
) else (
    :: ---------------------------------------------
    :: Create the Conda Environment
    :: This initializes a new Conda environment from the provided environment.yml file
    :: ---------------------------------------------
    start /wait cmd /c "call .\weights\miniconda\miniconda3\Scripts\activate.bat && conda env create --prefix .\venvpy_3.9 -f .\environment.yml"

    :: ---------------------------------------------
    :: Check if Conda Environment Creation was successful
    :: This ensures the script stops if the environment creation fails
    :: ---------------------------------------------
    if %errorlevel% neq 0 (
        echo Conda environment creation failed.
        exit /b %errorlevel%
    )
)

:: ---------------------------------------------
:: Run Redis server for caching
:: Redis needs to be running to handle cache operations for the app
:: ---------------------------------------------
start cmd /k "call .\weights\Redis-x64-3.0.504\redis-server.exe"

:: ---------------------------------------------
:: Run the Django Application
:: This starts the Django development server
:: ---------------------------------------------
start cmd /k "call .\weights\miniconda\miniconda3\Scripts\activate.bat && conda activate .\venvpy_3.9 && cd app && python manage.py runserver 0.0.0.0:8000"

:: ---------------------------------------------
:: Open a second command prompt window for Celery
:: Celery is used for asynchronous task processing
:: ---------------------------------------------
start cmd /k "call .\weights\miniconda\miniconda3\Scripts\activate.bat && conda activate .\venvpy_3.9 && cd app && celery -A app worker --loglevel=info -P eventlet"

:: ---------------------------------------------
:: Wait for 15 seconds before opening the web browser
:: ---------------------------------------------
timeout /t 15

:: ---------------------------------------------
:: Open a web browser to the Django application home page
:: ---------------------------------------------
start "" "http://127.0.0.1:8000/home/"












REM :: ---------------------------------------------
REM :: Add Environmental Variable for ffmpeg video encoder
REM :: This ensures ffmpeg is available system-wide
REM :: ---------------------------------------------
REM setx Path "C:\B-Star\weights\ffmpeg-6.0-full_build\bin;%Path%"

REM :: ---------------------------------------------
REM :: Create the Conda Environment
REM :: This initializes a new Conda environment from the provided environment.yml file
REM :: ---------------------------------------------
REM start /wait cmd /c "call .\weights\miniconda\miniconda3\Scripts\activate.bat && conda env create --prefix C:\B-Star\venvpy_3.9 -f .\environment.yml"

REM :: ---------------------------------------------
REM :: Check if Conda Environment Creation was successful
REM :: This ensures the script stops if the environment creation fails
REM :: ---------------------------------------------
REM REM if %errorlevel% neq 0 (
    REM REM echo Conda environment creation failed.
    REM REM exit /b %errorlevel%
REM REM )

REM :: ---------------------------------------------
REM :: Run Redis server for caching
REM :: Redis needs to be running to handle cache operations for the app
REM :: ---------------------------------------------
REM start cmd /k "call .\weights\Redis-x64-3.0.504\redis-server.exe"

REM :: ---------------------------------------------
REM :: Run the Django Application
REM :: This starts the Django development server
REM :: ---------------------------------------------
REM start cmd /k "call .\weights\miniconda\miniconda3\Scripts\activate.bat && conda activate C:\B-Star\venvpy_3.9 && cd app && python manage.py runserver 0.0.0.0:8000"

REM :: ---------------------------------------------
REM :: Open a second command prompt window for Celery
REM :: Celery is used for asynchronous task processing
REM :: ---------------------------------------------
REM start cmd /k "call .\weights\miniconda\miniconda3\Scripts\activate.bat && conda activate C:\B-Star\venvpy_3.9 && cd app && celery -A app worker --loglevel=info -P eventlet"

REM :: ---------------------------------------------
REM :: Wait for 15 seconds before opening the web browser
REM :: ---------------------------------------------
REM timeout /t 15

REM :: ---------------------------------------------
REM :: Open a web browser to the Django application home page
REM :: ---------------------------------------------
REM start "" "http://127.0.0.1:8000/home/"
