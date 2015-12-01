
def g2( x ):
   xbl=x
   for xi in range(0,x.shape[0]):
      xbl[xi,:]=x[xi,:]-x[xi,:].mean()
   kur=xbl
   FIXME - do all the power stuff
   return kur;



# function G2=g2(x)
# % x is a data matrix (or a vector), raws for channels, columns for time samples.
# if size(x,2)==1
#     x=x';
# end
# if size(x,1)==1
#     xbl=x-mean(x,2);
# else
#     xbl=x-vec2mat(mean(x,2),size(x,2));
# end
# x2=xbl.^2;
# x4=xbl.^4;
# sx2=sum(x2')';
# sx4=sum(x4')';
# VAR=sx2./(size(x,2)-1);
# G2=sx4./(VAR.*VAR.*size(x,2))-3; %here the -3 was deleted to avoid negative g2.
# end
