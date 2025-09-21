from flask import Flask, request, jsonify
import sys
sys.path.append('..')
import os
from mace.calculators import MACECalculator
import torch
from ase.io import read
from fileIO import parse_ifile, write_ofile
from ase.units import eV, Angstrom, Hartree, Bohr
from ase.io import read
import io

# 全部采用ase的单位换算
eV_To_hartree = eV/Hartree
Angs_To_bohr = Angstrom/Bohr
eV_ANGs_TO_hartree_bohr = eV_To_hartree/Angs_To_bohr
eV_sq_ANGs_TO_hartree_sq_bohr = eV_To_hartree/(Angs_To_bohr ** 2)

app = Flask(__name__)
# load mace model并持久化
model_path = r'./models/mace_model/final_Rh_all_nms-f_stagetwo.model'
app.config['model'] = MACECalculator(model_paths=model_path, device='cuda')

@app.route('/predict', methods=['POST'])
def predict():

    # 获取表单中的 natoms
    natoms = int(request.form['natoms'])

    # 获取上传的 XYZ 文件
    xyz_file = request.files['xyz_file']
    xyz_content = xyz_file.read().decode('utf-8')  # 读取文件内容并解码为字符串
    # 将 XYZ 字符串转换回 ASE 的 Atoms 对象
    xyz_io = io.StringIO(xyz_content)
    mol = read(xyz_io, format='xyz')

    print('run ts optimization by RMLP')

    calculator = app.config['model']  # 使用持久化的模型
    mol.calc = calculator

    energy = mol.get_total_energy() * eV_To_hartree
    grad = - mol.get_forces() * eV_ANGs_TO_hartree_bohr

    # 纯MACE模型可以直接导出解析hessian
    hessian3d = mol.calc.get_hessian() * eV_sq_ANGs_TO_hartree_sq_bohr  # 模型梯度二阶导数的Hessian
    hessian = hessian3d.reshape(natoms * 3, natoms * 3)  # 转换为2维的Hessian

    # 返回预测结果
    return jsonify({'energy': energy, 'grad': grad.tolist(), 'hessian': hessian.tolist()})

if __name__ == "__main__":

    app.run(host='0.0.0.0', port=5000)  # 启动服务器，监听所有外部 IP




