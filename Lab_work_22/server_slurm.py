import subprocess
import os
import glob

input_dir = 'gaussian_inputs'
gjf_files = sorted(glob.glob(f'{input_dir}/*.gjf'))

# Создание скрипта задания для каждого расчёта
for gjf_file in gjf_files:
    base_name = os.path.basename(gjf_file).replace('.gjf', '')
    
    job_script = f"""#!/bin/bash
#SBATCH --job-name={base_name}
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=02:00:00
#SBATCH --output={base_name}.out

module purge
module load gaussian/16
g16 {gjf_file}
"""
    
    with open(f'{base_name}.sh', 'w') as f:
        f.write(job_script)
    
    # Отправка задания в очередь
    subprocess.run(['sbatch', f'{base_name}.sh'])
    print(f"✓ Отправлено в очередь: {base_name}")

print("\nВсе задания отправлены. Используйте 'squeue -u $USER' для мониторинга.")