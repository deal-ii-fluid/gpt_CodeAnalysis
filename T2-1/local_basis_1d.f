      subroutine local_basis_1d ( order, node_x, x, phi )

c*********************************************************************72
c
cc LOCAL_BASIS_1D evaluates the basis functions in an element.
c
c  Discussion:
c
c    PHI(I)(X) = product ( J ~= I ) ( X         - NODE_X(I) )
c                                 / ( NODE_X(J) - NODE_X(I) )
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

      integer i
      integer j
      double precision node_x(order)
      double precision phi(order)
      double precision x

      do i = 1, order
        phi(i) = 1.0D+00
      end do

      do i = 1, order
        do j = 1, order
          if ( j .ne. i ) then
            phi(j) = ( phi(j) * ( x - node_x(i) ) ) 
     &        / ( node_x(j) - node_x(i) )
          end if
        end do
      end do

      return
      end
