      SUBROUTINE PS_SVD_1(LARGE,T,TPS,
     .                   SEVBAK,VTRA,DIAGV,RV1,CEREP,NM,NKN)
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
      end 
