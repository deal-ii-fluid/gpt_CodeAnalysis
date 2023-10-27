子程序[attach_3d]: 将具有在“pnode”中的坐标的节点连接到包含在字段“pneigh”中具有坐标的“nterms”个节点的面。
1. 参数：
   pneigh: [实数数组]，包含“nterms”个节点坐标的二维数组。
   pnode: [实数数组]，节点的三维坐标。
   nterms: [整数]，包含在pneigh中的节点数目。
   ratio: [实数数组]，节点的比例值。
   dist: [实数]，节点与面之间的距离。
   xil, etl, zel: [实数]，节点相对于面的位置。
   loopa: [整数]，循环次数。
2. 具体功能：
   此子程序将具有在“pnode”中的坐标的节点连接到包含在字段“pneigh”中的“nterms”个节点的面。
   它通过在(-1,1)x(-1,1)x(-1,1)的区域内生成一个3x3x3的矩阵，并计算每个点与面之间的距离来找到最佳连接点。
3. 算法实现：
   a. 初始化变量和数组。
   b. 计算初始连接点与面之间的距离并记录最小值及其对应的坐标。
   c. 循环进行以下步骤：
      - 缩小3x3x3矩阵的范围。
      - 计算每个点与面之间的距离并更新最小值及其对应的坐标。
      - 如果找到了最小值为0的连接点，则退出循环。
   d. 计算最佳连接点与面之间的距离及其坐标。
   e. 根据节点数目选择不同的计算方式，更新节点相对于面的位置。
   f. 返回值。
4. 注意事项：
   - 输入的节点坐标存储在pnode数组中，大小为(3)。
   - 输入的包含节点坐标的数组存储在pneigh数组中，大小为(3,20)。
   - 节点数目nterms必须小于20。
   - 输出的节点相对于面的位置存储在xil, etl, zel中。
   - 如果找到的最小连接距离为0，则表示已找到最佳连接点，循环将终止。
5. UML图：
   @startuml
   start
   :初始化变量;
   :计算初始连接距离;
   repeat
       :缩小矩阵范围;
       :计算连接距离并更新最小值和坐标;
       if (找到最小值为0的连接点?) then (是)
           stop
       else (否)
           continue
       endif
   repeat while (循环条件满足?);
   :计算最佳连接点距离和坐标;
   :根据节点数目更新节点相对于面的位置;
   stop
   @enduml
```