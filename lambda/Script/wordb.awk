BEGIN {

    N = length(WORD);

    VOW = "aeiou";
    GLI = "yw";
    CNS = "bcdfghjklmnpqrstvxz";

    LET = VOW GLI CNS;

    # Universe consisting of 0 as a dummy value in functions,
    # positions 1 through N,
    # and letter types for vowels, glides, and consonants.
    printf("universe = {0,")
    for (i=1;i<=N;i++){
	printf("%s,",i)
    }
    for (i=1;i<=length(LET);i++){
	printf("%s",substr(LET,i,1))
	if (i < length(LET)) printf(",");
    }
    printf("}.\n")

    # Specify extension of the Vow predicate.
    printf("predicate Vow = {")
    for (i=1;i<=length(VOW);i++){
	printf("%s",substr(VOW,i,1))
	if (i < length(VOW)) printf(",");
    }
    printf("}.\n")

    # Specify extension of the Cns predicate.
    printf("predicate Cns = {")
    for (i=1;i<=length(CNS);i++){
	printf("%s",substr(CNS,i,1))
	if (i < length(CNS)) printf(",");
    }
    printf("}.\n")

    # Specify extension of the Gli predicate.
    printf("predicate Gli = {")
    for (i=1;i<=length(GLI);i++){
	printf("%s",substr(GLI,i,1))
	if (i < length(GLI)) printf(",");
    }
    printf("}.\n")

    # Specify extension of the Pos (position) predicate.
    printf("predicate Pos = {")
    for (i=1;i<=N;i++){
	printf("%s",i)
	if (i < N) printf(",");
    }
    printf("}.\n")

    # Successor relation on positions. In word1, it's the adjacency relation.
    printf("predicate D = {")
    for (i=1;i<N;i++){
	printf("<%s,%s>,",i,i+1)
	printf("<%s,%s>",i+1,i)
	if (i+1 < N) printf(",");
    }
    printf("}.\n")

    # Constants for the positions.
    for (i=1;i<=N;i++){
	printf("constant N%s = %s.\n",i,i)
    }

    # Function mapping positions to letters defines the string.
    # 0 is a dummy value for other individuals.
    printf("function C = {")
    for (i=1;i<=N;i++){
	printf("<%s>=%s,", i, substr(WORD,i,1))
    }
    for (i=1;i<=length(LET);i++){
	printf("<%s>=0,",substr(LET,i,1))
    }
    printf("<0> = 0}.\n")


}