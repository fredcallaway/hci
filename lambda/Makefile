.PRECIOUS: %.in %.plw

# When running on your own machne, you need to install flex
# and compile the program fml.
Script/fml:	Script/fml.l
	flex Script/fml.l
	gcc lex.yy.c -ll 
	mv a.out Script/fml
	chmod +x Script/fml


instructions3.pdf: instructions3.txt
	enscript -o instructions3.ps instructions3.txt
	ps2pdf instructions3.ps

%.fml: %.tex Script/fml
	cat $*.tex | egrep 'result' | head -1 | Script/fml

%.plw:
	awk -f Script/word.awk -v WORD=$* > $*.plw

%.pl1:
	awk -f Script/word1.awk -v WORD=$* > $*.pl1

%.pl2:
	awk -f Script/word2.awk -v WORD=$* > $*.pl2

%.pl3:
	awk -f Script/word3.awk -v WORD=$* > $*.pl3

%.out:	%.in
	java -jar ../java/Plop.jar $*.in > $*.out

# The java programs should be ../java/Plop.jar and ../java/Lambda.jar
%.out3:	%.in
	java -jar ../java/Plop.jar $*.in3 > $*.out3

%.in:
	make $(word 1,$(subst ., ,$*)).plw
	cp $(word 2,$(subst ., ,$*)).fml $*.in
	cat $(word 1,$(subst ., ,$*)).plw >> $*.in

%.in1:
	make $(word 1,$(subst ., ,$*)).pl1
	cp $(word 2,$(subst ., ,$*)).fml $*.in1
	cat $(word 1,$(subst ., ,$*)).pl1 >> $*.in1

%.in2:
	make $(word 1,$(subst ., ,$*)).pl2
	cp $(word 2,$(subst ., ,$*)).fml $*.in2
	cat $(word 1,$(subst ., ,$*)).pl2 >> $*.in2

%.in3:
	make $(word 1,$(subst ., ,$*)).pl3
	cp $(word 2,$(subst ., ,$*)).fml $*.in3
	cat $(word 1,$(subst ., ,$*)).pl3 >> $*.in3
clean:
	rm *.in *.out *.plw *.aux *.ps *.pdf *.log

