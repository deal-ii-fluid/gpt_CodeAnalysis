      subroutine local_basis_prime_1d ( order, node_x, x, dphidx )

c*********************************************************************72
c
cc LOCAL_BASIS_PRIME_1D evaluates the basis function derivatives in an element.
c
c  Discussion:
c
c    PHI(I)(X) = product ( J ~= I ) ( X - NODE_X(I) )
c                                 / ( NODE_X(J) - NODE_X(I) )
c
c    dPHIdx(I)(X) = sum ( J ~= I ) ( 1 / ( NODE_X(J) - NODE_X(I) ) *
c      product ( K ~= ( J, I ) ) ( X - NODE_X(I) ) / ( NODE_X(J) - NODE_X(I) )
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
c    John Burkardt
c
c  Parameters:
c
c    Input, integer ORDER, the order of the element.
c    0 <= ORDER.  ORDER = 1 means piecewise linear.
c
c    Input, double precision NODE_X(ORDER), the element nodes.
c    These must be distinct.  Basis function I is 1 when X = NODE_X(I)
c    and 0 when X is equal to any other node.
c
c    Input, double precision X, the point at which the basis functions are to
c    be evaluated.
c
c    Output, double precision PHI(ORDER), the basis functions.
c
      implicit none

      integer order

      double precision dphidx(order)
      integer i
      integer j
      integer k
      double precision node_x(order)
      double precision term
      double precision x

      do i = 1, order
        dphidx(i) = 0.0D+00
      end do

      do i = 1, order
        do j = 1, order
          if ( j .ne. i ) then
            term = 1.0D+00 / ( node_x(j) - node_x(i) )
            do k = 1, order
              if ( k .ne. i .and. k .ne. j ) then
                term = term * ( x - node_x(i) ) 
     &            / ( node_x(k) - node_x(i) )
              end if
            end do
            dphidx(i) = dphidx(i) + term
          end if
        end do
      end do

      return
      end
