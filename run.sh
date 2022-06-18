npass=0
nfail=0
testnum=1
skip="__pycache__"
for d in goldenFiles/*/ ; do
    name=$(basename "$d")
    if [[ "$name" != "$skip" ]]; then
        echo "---------------- TEST #$testnum $name -------------------"
        make test case="$name"
        output=$(python3 -Wi goldenFiles/testChecker.py "$name")
        if [[ $? -eq 0 ]]; then
            ((++npass))
        else
            ((++nfail))
        fi
        echo "$output"
        echo -e "---------------- TEST #$testnum $name -------------------\n"
        ((++testnum))
    fi
done
echo "$npass out of $(($npass + $nfail)) test cases have passed!"
exit $nfail
