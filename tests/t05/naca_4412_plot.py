# Importing necessary modules
import os
import csv
    
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def main():
   
    # Running the user's provided code again
    
    # 实际输出比例,单位mm
    scaleX=40 
    scaleY=40
    scaleZ=38.5
    
    # NACA 4412参数
    M = 0.04
    P = 0.4
    T = 0.12
    
    # 厚度分布常数
    a0, a1, a2, a3, a4 = 0.2969, -0.126, -0.3516, 0.2843, -0.1036
    
    # 计算翼型形状
    beta1 = np.linspace(0, 8/10*np.pi, 150)
    beta2 = np.linspace(8/10*np.pi, np.pi, 500)
    beta = np.concatenate((beta1, beta2))
    #beta = np.linspace(0, np.pi, 2000)
    x = (1 - np.cos(beta)) / 2
    yc = np.where(x < P, M/(P**2) * (2*P*x - x**2), M/((1-P)**2) * (1 - 2*P + 2*P*x - x**2))
    dyc_dx = np.where(x < P, 2*M/(P**2) * (P - x), 2*M/((1-P)**2) * (P - x))
    
    # 定义z范围
    z_values = np.linspace(0, 1.0, 4400)
    
    
    # 初始化3D图
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # 设置X和Y轴为相同的比例
    max_range = np.array([x.max()-x.min(), yc.max()-yc.min(), z_values.max()-z_values.min()]).max() / 2.0
    mid_x = (x.max()+x.min()) * 0.5
    mid_y = (yc.max()+yc.min()) * 0.5
    mid_z = (z_values.max()+z_values.min()) * 0.5
    ax.set_xlim((mid_x - max_range)*scaleX, (mid_x + max_range)*scaleY)
    ax.set_ylim((mid_y - max_range)*scaleX, (mid_y + max_range)*scaleY)
    ax.set_zlim(0, 1.1*scaleZ)
    
    # 绘制每个z值的翼型形状
    for z in z_values:
        a4_mod = -0.1036 * (1 + 0.3 * np.cos(6*2 * np.pi * z))
        yt = (T / 0.2) * (a0 * np.sqrt(x) + a1 * x + a2 * x**2 + a3 * x**3 + a4_mod * x**4)
        theta = np.arctan(dyc_dx)
        xu, yu = x - yt * np.sin(theta), yc + yt * np.cos(theta)
        xl, yl = x + yt * np.sin(theta), yc - yt * np.cos(theta)
        
        # 计算上下表面之间的差异并找到交点
        y_diff = yu - yl
        zero_crossings = np.where(np.logical_and(np.diff(np.sign(y_diff)), x[:-1] > 0.0001))[0]
        if zero_crossings.size:
            idx = zero_crossings[0]
            xu, yu = xu[:idx+1], yu[:idx+1]
            xl, yl = xl[:idx+1], yl[:idx+1]
        
        ax.plot(xu*scaleX, yu*scaleY, z*scaleZ, color='blue', lw=0.5)
        ax.plot(xl*scaleX, yl*scaleY, z*scaleZ, color='blue', lw=0.5)
    
    # 设置图参数
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D View of Stretched NACA 4412 Airfoil with Modified $a_4$ Parameter (Equal Scale for X and Y)')
    ax.view_init(elev=20, azim=-60)
    
    
    # Now, let's proceed to generate the CSV files.
    # Create a directory to store all the CSV files
    output_dir = "/home/wjq/Programming/nix/02-cloud-point-lib/01-naca4412/data"
    os.makedirs(output_dir, exist_ok=True)
   
    with open(f"{output_dir}/point_cloud.txt", "w") as file:
        # Write data to txt files for each z value
        for idx, z in enumerate(z_values):
            a4_mod = -0.1036 * (1 + 0.3 * np.cos(6*2 * np.pi * z))
            yt = (T / 0.2) * (a0 * np.sqrt(x) + a1 * x + a2 * x**2 + a3 * x**3 + a4_mod * x**4)
            theta = np.arctan(dyc_dx)
            xu, yu = x - yt * np.sin(theta), yc + yt * np.cos(theta)
            xl, yl = x + yt * np.sin(theta), yc - yt * np.cos(theta)

            # 计算上下表面之间的差异并找到交点
            y_diff = yu - yl
            zero_crossings = np.where(np.logical_and(np.diff(np.sign(y_diff)), x[:-1] > 0.0001))[0]
            if zero_crossings.size:
                idx_cross = zero_crossings[0]
                xu, yu = xu[:idx_cross+1], yu[:idx_cross+1]
                xl, yl = xl[:idx_cross+1], yl[:idx_cross+1]

            # Write upper surface to txt
            for i, (x_val, y_val) in enumerate(zip(xu, yu)):
                file.write(f"{x_val*scaleX} {y_val*scaleY} {z*scaleZ}\n")

            for i, (x_val, y_val) in enumerate(zip(xl, yl)):
                file.write(f"{x_val*scaleX} {y_val*scaleY} {z*scaleZ}\n")


    

if __name__ == "__main__":
    main()


