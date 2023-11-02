      subroutine legendre_com ( norder, xtab, weight )

c*********************************************************************72
c
cc LEGENDRE_COM computes abscissas and weights for Gauss-Legendre quadrature.
c
c  Integration interval:
c
c    [ -1, 1 ]
c
c  Weight function:
c
c    1.
c
c  Integral to approximate:
c
c    Integral ( -1 <= X <= 1 ) F(X) dX.
c
c  Approximate integral:
c
c    sum ( 1 <= I <= NORDER ) WEIGHT(I) * F ( XTAB(I) ).
c
c  Licensing:
c
c    This code is distributed under the GNU LGPL license.
c
c  Modified:
c
c    04 July 2013
c
c  Author:
c
c    Original FORTRAN77 version by Philip Davis, Philip Rabinowitz
c    This FORTRAN77 version by John Burkardt.
c
c  Parameters:
c
c    Input, integer NORDER, the order of the rule.
c    NORDER must be greater than 0.
c
c    Output, double precision XTAB(NORDER), the abscissas of the rule.
c
c    Output, double precision WEIGHT(NORDER), the weights of the rule.
c    The weights are positive, symmetric, and should sum to 2.
c
      implicit none

      integer norder

      double precision d1
      double precision d2pn
      double precision d3pn
      double precision d4pn
      double precision dp
      double precision dpn
      double precision e1
      double precision fx
      double precision h
      integer i
      integer iback
      integer k
      integer m
      integer mp1mi
      integer ncopy
      integer nmove
      double precision p
      double precision pi
      parameter ( pi = 3.141592653589793D+00 )
      double precision pk
      double precision pkm1
      double precision pkp1
      double precision t
      double precision u
      double precision v
      double precision x0
      double precision xtab(norder)
      double precision xtemp
      double precision weight(norder)

      if ( norder .lt. 1 ) then
        write ( *, '(a)' ) ' '
        write ( *, '(a)' ) 'LEGENDRE_COM - Fatal error!'
        write ( *, '(a,i8)' ) '  Illegal value of NORDER = ', norder
        stop
      end if

      e1 = dble ( norder * ( norder + 1 ) )

      m = ( norder + 1 ) / 2

      do i = 1, ( norder + 1 ) / 2

        mp1mi = m + 1 - i
        t = pi * dble ( 4 * i - 1 ) / dble ( 4 * norder + 2 )
        x0 = cos(t) * ( 1.0D+00 - ( 1.0D+00 - 1.0D+00 
     &    / dble ( norder ) ) / dble ( 8 * norder * norder ) )

        pkm1 = 1.0D+00
        pk = x0

        do k = 2, norder
          pkp1 = 2.0D+00 * x0 * pk - pkm1 - ( x0 * pk - pkm1 ) 
     &      / dble ( k )
          pkm1 = pk
          pk = pkp1
        end do

        d1 = real ( norder, kind = 8 ) * ( pkm1 - x0 * pk )

        dpn = d1 / ( 1.0D+00 - x0 * x0 )

        d2pn = ( 2.0D+00 * x0 * dpn - e1 * pk ) / ( 1.0D+00 - x0 * x0 )

        d3pn = ( 4.0D+00 * x0 * d2pn + ( 2.0D+00 - e1 ) * dpn ) /       
     &    ( 1.0D+00 - x0 * x0 )

        d4pn = ( 6.0D+00 * x0 * d3pn + ( 6.0D+00 - e1 ) * d2pn ) /
     &    ( 1.0D+00 - x0 * x0 )

        u = pk / dpn
        v = d2pn / dpn
c
c  Initial approximation H:
c
        h = - u * ( 1.0D+00 + 0.5D+00 * u * ( v + u * ( v * v - d3pn    
     &   / ( 3.0D+00 * dpn ) ) ) )
c
c  Refine H using one step of Newton's method:
c
        p = pk + h * ( dpn + 0.5D+00 * h * ( d2pn + h / 3.0D+00 * 
     &    ( d3pn + 0.25D+00 * h * d4pn ) ) )

        dp = dpn + h * ( d2pn + 0.5D+00 * h * ( d3pn + h * d4pn 
     &    / 3.0D+00 ) )

        h = h - p / dp

        xtemp = x0 + h

        xtab(mp1mi) = xtemp

        fx = d1 - h * e1 * ( pk + 0.5D+00 * h * ( dpn + h / 3.0D+00     
     &    * ( d2pn + 0.25D+00 * h * ( d3pn + 0.2D+00 * h * d4pn ) ) ) )

        weight(mp1mi) = 2.0D+00 * ( 1.0D+00 - xtemp * xtemp ) 
     &    / ( fx * fx )

      end do

      if ( mod ( norder, 2 ) .eq. 1 ) then
        xtab(1) = 0.0D+00
      end if
c
c  Shift the data up.
c
      nmove = int ( ( norder + 1 ) / 2 )
      ncopy = norder - nmove

      do i = 1, nmove
        iback = norder + 1 - i
        xtab(iback) = xtab(iback-ncopy)
        weight(iback) = weight(iback-ncopy)
      end do
c
c  Reflect values for the negative abscissas.
c
      do i = 1, norder - nmove
        xtab(i) = - xtab(norder+1-i)
        weight(i) = weight(norder+1-i)
      end do

      return
      end
