      subroutine local_fem_1d ( order, node_x, node_v, sample_num, 
     &  sample_x, sample_v )

c*********************************************************************72
c
cc LOCAL_FEM_1D evaluates a local finite element function.
c
c  Discussion:
c
c    A local finite element function is a finite element function
c    defined over a single element.
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
c    These must be distinct.  Basis function I is 1 when X = NODE_X(I) and 0
c    when X is equal to any other node.
c
c    Input, double precision NODE_V(ORDER), the value of the finite element
c    function at each node.
c
c    Input, integer SAMPLE_NUM, the number of sample points.
c
c    Input, double precision SAMPLE_X(SAMPLE_NUM), the sample points at which
c    the local finite element function is to be evaluated.
c
c    Output, double precision SAMPLE_V(SAMPLE_NUM), the values of the local
c    finite element basis functions.
c
      implicit none

      integer order
      integer sample_num

      integer i
      double precision node_v(order)
      double precision node_x(order)
      double precision phi(order)
      double precision r8vec_dot_product
      integer sample
      double precision sample_v(sample_num)
      double precision sample_x(sample_num)
      double precision x

      do i = 1, sample_num
        sample_v(i) = 0.0D+00
      end do

      do sample = 1, sample_num

        x = sample_x(sample)
        call local_basis_1d ( order, node_x, x, phi )
        sample_v(sample) = r8vec_dot_product ( order, node_v, phi )

      end do

      return
      end
