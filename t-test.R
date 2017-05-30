iris<-read.csv("/Users/chaoran/Desktop/Direct Study/Direct Study iris%.csv")
tictac<-read.csv("/Users/chaoran/Desktop/Direct Study/Direct Study ttt%.csv")

#iris before and after
irisB<-iris$before..f
irisA<-iris$after.f
t.test(irisB, irisA, paired=TRUE)

#tic tac toe before and after
tictacB<-tictac$before.f
tictacA<-tictac$after.f
t.test(tictacB, tictacA, paired=TRUE)