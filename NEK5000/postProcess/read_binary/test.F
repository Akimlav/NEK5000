	program test
	implicit none

	integer na,i,n
	parameter(n=10,na=12345)
	double precision,dimension(n)::xp,yp,zp
	double precision time

	call RANDOM_NUMBER(time)
	call RANDOM_NUMBER(xp)
	call RANDOM_NUMBER(yp)
	call RANDOM_NUMBER(zp)

        open(unit=11,file="fortran_bin",form='unformatted')
 	write(11) time,na
	do i=1,n
	write(11)i,xp(i),yp(i),zp(i)
	end do
	close(11)

        open(unit=12,file="fortran_ascii.dat",status="unknown")
 	write(12,fmt='(F20.12,I7)') time,na
	do i=1,n
	write(12,fmt='(I7,3F20.12)')i,xp(i),yp(i),zp(i)
	end do
	close(12)

	end
