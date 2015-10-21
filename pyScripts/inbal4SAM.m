cd /home/yuval/Data/inbal/4/SAM
[~, ~,wts]=readWeights('pnt.txt.wts');
cd ../
avg=importdata('avg.txt');
figure;
topoplot248(avg(:,388),[],1);

fwd=mne_read_forward_solution('4_raw-oct-6-fwd.fif');
lh=fwd.src(1).rr(fwd.src(1).vertno,:);
rh=fwd.src(2).rr(fwd.src(2).vertno,:);
brain=[lh;rh];
% change from LPI to PRI order
brain=brain(:,[2,1,3]);
brain(:,2)=-brain(:,2);
figure;
plot3pnt(brain,'.')
hold on
plot3pnt(hs.pnt,'ok')


chanInd=[186,2,46,148,57,150,218,15,14,50,42,66,34,152,154,19,223,224,118,12,120,1,219,85,39,8,101,32,172,162,62,125,188,222,21,159,23,81,10,182,216,87,111,246,74,214,43,241,139,71,206,196,200,133,124,91,89,128,158,129,149,119,48,45,13,86,52,143,176,40,7,41,202,171,105,70,208,60,131,97,166,28,220,122,126,90,192,130,193,217,83,215,9,153,16,88,178,38,76,110,180,113,136,3,68,239,108,165,163,233,234,26,100,17,53,92,190,227,195,95,147,117,183,181,11,151,51,142,209,109,210,114,244,247,103,204,102,5,138,230,94,197,99,231,135,127,189,191,226,156,93,229,184,221,49,141,177,245,144,44,146,238,137,173,35,140,104,61,132,24,167,164,169,55,18,59,47,185,187,75,80,213,115,205,236,67,240,72,96,199,22,201,155,56,161,243,212,211,116,112,170,30,134,36,174,107,25,228,232,98,198,84,123,6,78,248,179,168,65,31,242,69,63,27,160,203,157,20,121,82,73,175,37,77,79,145,207,29,33,106,4,58,194,235,64,237,54,225,];
source=wts(:,chanInd)*avg;
BL=zeros(8196,1);
sourceNorm=zeros(size(source));
for i=1:8196
    %BL(i)=mean(source(i,102:305));
%     BL(i)=mean(abs(wts(i,:)));
%     sourceNorm(i,:)=source(i,:)./BL(i);
    
    sourceNorm(i,:)=source(i,:)-mean(source(i,102:305));
    sourceNorm(i,:)=sourceNorm(i,:)./median(abs(sourceNorm(i,:)));
end


figure;scatter3pnt(brain,13,abs(sourceNorm(:,388)))
figure;scatter3pnt(brain,13,abs(mean(sourceNorm(:,380:400),2)))
figure;scatter3pnt(brain,13,abs(mean(sourceNorm(:,420:450),2)))
figure;scatter3pnt(brain,13,abs(mean(sourceNorm(:,500:540),2)))
figure;topoplot248(mean(avg(:,420:450),2),[],1)
%% Nwts 3 days, take care
cd /home/yuval/Data/inbal/4
fwd=mne_read_forward_solution('4_raw-oct-6-fwd.fif');
lh=fwd.src(1).rr(fwd.src(1).vertno,:);
rh=fwd.src(2).rr(fwd.src(2).vertno,:);
brain=[lh;rh];
brain=brain(:,[2,1,3]);
brain(:,2)=-brain(:,2);

clear *h

cd /home/yuval/Data/inbal
X=zeros(length(brain),1);
Y=X;
Z=X;
Nwts=zeros(8196,248);
parfor pnti=1:8196
    unix(['echo 8 > 4/SAM/Tetra',num2str(pnti),'.txt']);
    X(pnti)=brain(pnti,1)*100;
    Y(pnti)=brain(pnti,2)*100;
    Z(pnti)=brain(pnti,3)*100;
    unix(['echo "',num2str(X(pnti)),' ',num2str(Y(pnti)),' ',num2str(Z(pnti)),'" >> 4/SAM/Tetra',num2str(pnti),'.txt']);
    unix(['echo "',num2str(X(pnti)-1),' ',num2str(Y(pnti)),' ',num2str(Z(pnti)),'" >> 4/SAM/Tetra',num2str(pnti),'.txt']);
    unix(['echo "',num2str(X(pnti)+1),' ',num2str(Y(pnti)),' ',num2str(Z(pnti)),'" >> 4/SAM/Tetra',num2str(pnti),'.txt']);
    unix(['echo "',num2str(X(pnti)),' ',num2str(Y(pnti)-1),' ',num2str(Z(pnti)),'" >> 4/SAM/Tetra',num2str(pnti),'.txt']);
    unix(['echo "',num2str(X(pnti)),' ',num2str(Y(pnti)+1),' ',num2str(Z(pnti)),'" >> 4/SAM/Tetra',num2str(pnti),'.txt']);
    unix(['echo "',num2str(X(pnti)),' ',num2str(Y(pnti)),' ',num2str(Z(pnti)-1),'" >> 4/SAM/Tetra',num2str(pnti),'.txt']);
    unix(['echo "',num2str(X(pnti)),' ',num2str(Y(pnti)),' ',num2str(Z(pnti)+1),'" >> 4/SAM/Tetra',num2str(pnti),'.txt']);
    unix(['echo "',num2str(X(pnti)),' ',num2str(-Y(pnti)),' ',num2str(Z(pnti)),'" >> 4/SAM/Tetra',num2str(pnti),'.txt'])
    unix(['SAMNwts64 -r 4 -d rs,xc,hb,lf_c,rfhp0.1Hz -m aud -c Aa -t Tetra',num2str(pnti),'.txt -v']);
    [~, ~, NWgts]=readWeights(['4/SAM/aud,Tetra',num2str(pnti),'.txt.wts']);
    Nwts(pnti,:)=NWgts(1,:);
    disp(['XXXXXXXXX ',num2str(length(dir('4/SAM/aud,Tetra*.txt.wts'))),' XXXXXXXXXXX']);
end
save 4/SAM/Nwts8 Nwts
!rm 4/SAM/Tetra*.txt
!rm 4/SAM/aud*.txt.wts
%%
cd /home/yuval/Data/inbal
load 4/SAM/Nwts8
avg=importdata('4/avg.txt');

chanInd=[186,2,46,148,57,150,218,15,14,50,42,66,34,152,154,19,223,224,118,12,120,1,219,85,39,8,101,32,172,162,62,125,188,222,21,159,23,81,10,182,216,87,111,246,74,214,43,241,139,71,206,196,200,133,124,91,89,128,158,129,149,119,48,45,13,86,52,143,176,40,7,41,202,171,105,70,208,60,131,97,166,28,220,122,126,90,192,130,193,217,83,215,9,153,16,88,178,38,76,110,180,113,136,3,68,239,108,165,163,233,234,26,100,17,53,92,190,227,195,95,147,117,183,181,11,151,51,142,209,109,210,114,244,247,103,204,102,5,138,230,94,197,99,231,135,127,189,191,226,156,93,229,184,221,49,141,177,245,144,44,146,238,137,173,35,140,104,61,132,24,167,164,169,55,18,59,47,185,187,75,80,213,115,205,236,67,240,72,96,199,22,201,155,56,161,243,212,211,116,112,170,30,134,36,174,107,25,228,232,98,198,84,123,6,78,248,179,168,65,31,242,69,63,27,160,203,157,20,121,82,73,175,37,77,79,145,207,29,33,106,4,58,194,235,64,237,54,225,];
source=Nwts(:,chanInd)*avg;

BL=zeros(8196,1);
sourceNorm=zeros(size(source));
for i=1:8196
    %BL(i)=abs(mean(source(i,102:305)));
    %BL(i)=mean(abs(Nwts(i,:)));
    %sourceNorm(i,:)=source(i,:)./BL(i);
    
    sourceNorm(i,:)=source(i,:)-mean(source(i,102:305));
    sourceNorm(i,:)=sourceNorm(i,:)./median(abs(sourceNorm(i,:)));
end
vec=abs(mean(sourceNorm(:,380:400),2));
figure;scatter3pnt(brain,13,abs(mean(sourceNorm(:,380:400),2)))
figure;scatter3pnt(brain,13,abs(mean(sourceNorm(:,420:450),2)))
figure;scatter3pnt(brain,13,abs(mean(sourceNorm(:,500:540),2)))
figure;topoplot248(mean(avg(:,500:540),2),[],1)
times=importdata('/home/yuval/Data/inbal/4/times.txt');
ii=6611;
plot(times,sourceNorm(ii,:))