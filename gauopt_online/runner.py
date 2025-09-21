import sys
sys.path.append('..')
import os
import numpy as np
from fileIO import parse_ifile, write_ofile
from ase.units import eV, Angstrom, Hartree, Bohr

import io
import requests

# 全部采用ase的单位换算
eV_To_hartree = eV/Hartree
Angs_To_bohr = Angstrom/Bohr
eV_ANGs_TO_hartree_bohr = eV_To_hartree/Angs_To_bohr
eV_sq_ANGs_TO_hartree_sq_bohr = eV_To_hartree/(Angs_To_bohr ** 2)

def genxyz(atom_type, coordinates, path):

    num_atoms = len(atom_type)
    with open(path, 'w') as f:
        f.write(str(num_atoms) + '\n')
        f.write('\n')
        for i in range(num_atoms):
            f.write('{}\t{:.8f}\t{:.8f}\t{:.8f}\n'.format(atom_type[i], coordinates[i][0], coordinates[i][1],
                                                          coordinates[i][2]))
def genxyz_in_memory(atom_type, coordinates):
    """
    生成XYZ文件内容并返回为字符串而不是写入磁盘。
    """
    num_atoms = len(atom_type)
    xyz_content = f"{num_atoms}\n\n"  # XYZ文件格式：原子数量和空行
    for i in range(num_atoms):
        xyz_content += '{}\t{:.8f}\t{:.8f}\t{:.8f}\n'.format(atom_type[i], coordinates[i][0], coordinates[i][1],
                                                             coordinates[i][2])
    return xyz_content

if __name__ == "__main__":

    ifile = sys.argv[2]
    ofile = sys.argv[3]
    # ifile = './Gau-20020.EIn'  # 测试用例
    # ofile = './Gau-20020.EOu'

    # 解析输入文件
    (natoms, deriv, charge, spin, atomtypes, coordinates) = parse_ifile(ifile)

    # 生成XYZ格式的字符串内容（不写入文件）
    xyz_content = genxyz_in_memory(atomtypes, coordinates)
    # 准备POST请求的数据
    data = {'natoms': natoms}
    files = {'xyz_file': io.StringIO(xyz_content)}  # 将字符串内容转换为类似文件的对象传输

    # 创建一个持久会话
    session = requests.Session()
    try:
        # 发送文件和 natoms 的表单数据
        response = session.post("http://localhost:5000/predict", files=files, data=data)
        response.raise_for_status()  # 检查是否有 HTTP 错误
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        sys.exit(1)

    # 返回服务器响应
    energy = response.json()['energy']
    grad = np.array(response.json()['grad'])
    hessian = np.array(response.json()['hessian'])

    # 输出结果给高斯
    write_ofile(ofile, energy, natoms, gradient=grad, hessian=hessian)

