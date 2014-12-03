BEGIN {

    N = length(WORD);

    LVOW = "aeiou";
    CVOW = toupper(LVOW);
    VOW = LVOW CVOW;
    LGLI = "yw";
    CGLI = toupper(LGLI);
    GLI = LGLI CGLI;
    LCNS = "bcdfghjklmnpqrstvxz";
    CCNS = toupper(LCNS);
    CNS = LCNS CCNS;
    LET = VOW GLI CNS;
    CLET = CVOW CGLI CCNS;


    printf("universe = {0,")
    for (i=1;i<=N;i++){
	printf("%s,",i)
    }
    for (i=1;i<=length(LET);i++){
	printf("%s",substr(LET,i,1))
	if (i < length(LET)) printf(",");
    }
    printf("}.\n")


    printf("predicate Vow = {")
    for (i=1;i<=length(VOW);i++){
	printf("%s",substr(VOW,i,1))
	if (i < length(VOW)) printf(",");
    }
    printf("}.\n")


    printf("predicate Cns = {")
    for (i=1;i<=length(CNS);i++){
	printf("%s",substr(CNS,i,1))
	if (i < length(CNS)) printf(",");
    }
    printf("}.\n")


    printf("predicate Cap = {")
    for (i=1;i<=length(CLET);i++){
	printf("%s",substr(CLET,i,1))
	if (i < length(CLET)) printf(",");
    }
    printf("}.\n")


    printf("predicate Gli = {")
    for (i=1;i<=length(GLI);i++){
	printf("%s",substr(GLI,i,1))
	if (i < length(GLI)) printf(",");
    }
    printf("}.\n")


    printf("predicate Pos = {")
    for (i=1;i<=N;i++){
	printf("%s",i)
	if (i < N) printf(",");
    }
    printf("}.\n")


    printf("predicate D = {")
    for (i=1;i<N;i++){
	printf("<%s,%s>,",i,i+1)
	printf("<%s,%s>",i+1,i)
	if (i+1 < N) printf(",");
    }
    printf("}.\n")

    for (i=1;i<=N;i++){
	printf("constant N%s = %s.\n",i,i)
    }

    printf("function C = {")
    for (i=1;i<=N;i++){
	printf("<%s>=%s,", i, substr(WORD,i,1))
    }
    for (i=1;i<=length(LET);i++){
	printf("<%s>=0,",substr(LET,i,1))
    }
    printf("<0> = 0}.\n")
}