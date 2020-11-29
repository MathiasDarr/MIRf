import subprocess
import sys

if __name__ == '__main__':
    subprocess.run('bash -c "source activate /home/ubuntu/anaconda3/envs/tensorflow_p36 && python3 test_keras.py " ', shell=True)

