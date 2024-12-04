import sys
import os
import numpy as np
import requests
import requests_unixsocket  # 这是 Unix Socket 支持的 requests 库
import io
from fileIO import parse_ifile, write_ofile
from ase.units import eV, Angstrom, Hartree, Bohr

# 单位换算常量
eV_To_hartree = eV / Hartree
Angs_To_bohr = Angstrom / Bohr
eV_ANGs_TO_hartree_bohr = eV_To_hartree / Angs_To_bohr
eV_sq_ANGs_TO_hartree_sq_bohr = eV_To_hartree / (Angs_To_bohr ** 2)

def genxyz_in_memory(atom_type, coordinates):
    """
    生成 XYZ 文件内容，并返回字符串而不是写入磁盘
    """
    num_atoms = len(atom_type)
    xyz_content = f"{num_atoms}\n\n"  # XYZ 文件格式
    for i in range(num_atoms):
        xyz_content += '{}\t{:.8f}\t{:.8f}\t{:.8f}\n'.format(atom_type[i], coordinates[i][0], coordinates[i][1], coordinates[i][2])
    return xyz_content

if __name__ == "__main__":

    ifile = sys.argv[2]
    ofile = sys.argv[3]
    # ifile = './Gau-20020.EIn'  # 测试用例
    # ofile = './Gau-20020.EOu'

    # 解析输入文件，获取原子数量、坐标等
    (natoms, deriv, charge, spin, atomtypes, coordinates) = parse_ifile(ifile)

    # 生成 XYZ 格式的字符串内容
    xyz_content = genxyz_in_memory(atomtypes, coordinates)

    # 准备 POST 请求的数据
    data = {'natoms': str(natoms)}
    files = {'xyz_file': io.StringIO(xyz_content)}

    # 创建会话，并使用 Unix Socket 通信
    session = requests_unixsocket.Session()  # 这是 requests_unixsocket 专用的会话

    # Unix Socket URL 使用 requests_unixsocket 特定格式
    socket_path = "/home/tangkun/tmp/flask_server.sock"
    socket_url = "http+unix://%2Fhome%2Ftangkun%2Ftmp%2Fflask_server.sock/predict" # 注意 %2F

    try:
        # 发送 POST 请求并捕获响应
        response = session.post(socket_url, files=files, data=data)
        response.raise_for_status()  # 检查 HTTP 错误
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        sys.exit(1)

    # 解析响应数据
    energy = response.json()['energy']
    grad = np.array(response.json()['grad'])
    hessian = np.array(response.json()['hessian'])

    # 输出结果到指定输出文件
    write_ofile(ofile, energy, natoms, gradient=grad, hessian=hessian)
