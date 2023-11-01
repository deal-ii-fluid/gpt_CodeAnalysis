C
C    子程序 PS_SVD_1:通过奇异值分解获取伪逆解
C
C    输入参数:
C    LARGE - 控制参数
C    NM    - 矩阵的行数
C    NKN   - 矩阵的列数
C    T     - 原始矩阵
C
C    输出参数:
C    TPS   - 原始矩阵的伪逆
C    SEVBAK- 备份的敏感度矩阵
C    VTRA  - V 矩阵的转置
C    DIAGV - 奇异值对角矩阵
C
C    功能:
C    该子程序通过奇异值分解的方法计算矩阵的伪逆。首先，将原始矩阵复制到敏感度矩阵的备份中。
C    然后调用 SVDCMP 子程序进行奇异值分解，得到奇异值和 V 矩阵的转置。
C    接下来，对一些较小的奇异值进行处理，将其置零，以避免数值计算问题。
C    最后，通过矩阵运算计算原始矩阵的伪逆，结果存储在 TPS 中。
C
C    注意:
C    1. 奇异值分解是一种常用的数值稳定的矩阵分解方法，用于求解线性方程组和最小二乘问题。
C    2. 伪逆矩阵是原始矩阵的一种广义逆，可以用于求解过约束或欠约束的线性方程组。
C
C
c     ------------------------------------------------------------------
      SUBROUTINE PS_SVD_1(LARGE,T,TPS,
     .                   SEVBAK,VTRA,DIAGV,RV1,CEREP,NM,NKN)
C     ------------------------------------------------------------------
c
c.....Obtain the pseudo-inverse solution by SVD
c     nr. of equations > nr. of parameters
C     ------------------------------------------------------------------
c        nm:  number of rows
c        nkn: number of columns
c        t:   original matrix
c        tps: pseudo inverse of the original matrix
c        explicit code (matrix operations)
C     ------------------------------------------------------------------
C 
      INCLUDE    'systune.inc'
C
      INTEGER*4  LARGE(1),NM,NKN
      REAL*8     T(NM,NKN),TPS(NKN,NM),CEREP(*),
     .           SEVBAK(NM,NKN),VTRA(NKN,NKN),DIAGV(NKN),RV1(NM)
C
C                                                                              *
C     COPY SENSITIVITY MATRIX TO MATRIX SEVBAK(MAXPR,MAXPR)
C
      CALL INIT_R8_MATRIX(SEVBAK,NM,NM)
      DO 10 I    = 1, NM
      DO 10 J    = 1, NKN
         SEVBAK(I,J) = T(I,J)
   10 CONTINUE
C                                                                              *
C.....CALL FOR SINGULAER VALUE SOLUTION
C                                                                              *
      CALL INIT_R8_VECTOR(DIAGV,NKN)
      CALL INIT_R8_VECTOR(RV1,NM)
      CALL SVDCMP(SEVBAK,NM,NKN,DIAGV,VTRA,RV1,ERROR)
C                                                                              *
C.....ZEROR SOME SINGULAR VALUES
C                                                                              *
      SINMAX     = 0.
      DO 11 I    = 1, NKN
         IF (DIAGV(I) .GT. SINMAX) SINMAX = DIAGV(I)
   11 CONTINUE
      SINMIN     = SINMAX*1.0E-6
      DO 12 I    = 1, NKN
         IF (DIAGV(I) .LT. SINMIN) DIAGV(I) = 0.
   12 CONTINUE
C                                                                              *
C.....CALCULATION OF VTRA/DIAGV
      DO 14 J    = 1, NKN
      DO 15 I    = 1, NKN
         IF (DIAGV(J) .GT. SINMIN) THEN
            VTRA(I,J) = VTRA(I,J)/DIAGV(J)
         ELSE
            VTRA(I,J) = 0.
         END IF
   15 CONTINUE
   14 CONTINUE
C                                                                              *
C.....CALCULATION OF VTRA*(1/DIAGV)*SEVBAK(TRANSPOSE)
C                                                                              *
      DO 16 I    = 1, NKN
      DO 17 J    = 1, NM
         TPS(I,J)= 0.
         TMP =0.
         DO 18 K = 1, NKN
            IF (DIAGV(K) .GT. SINMIN) THEN
              TMP  = TMP + VTRA(I,K)*SEVBAK(J,K)
            END IF
   18    CONTINUE
         TPS(I,J)= TMP
   17 CONTINUE
   16 CONTINUE
C                                                                              *
      RETURN
C                                                                              *
      END 
