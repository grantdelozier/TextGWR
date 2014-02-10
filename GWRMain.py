import sys


if len(sys.argv) >= 3:
    #try:
    print sys.argv
    args = sys.argv
    mode_arg = args[args.index("-mode")+1]
    print mode_arg

    #############Build Reference File Mode###############
    if mode_arg.lower() == "build_ref_files":
        import BuildRef
        print "Building Reference Files"
        tf = args[args.index("-tf")+1]
        print tf
        rf_std_out = args[args.index("-rf_std_out")+1]
        print rf_std_out
        rf_obs_out = args[args.index("-rf_obs_out")+1]
        print rf_obs_out
        if '-wordlist' in args:
            wordlist = args[args.index("-wordlist")+1]
            if '-listuse' in args:
                listuse = args[args.index("-listuse")+1]
            else: listuse = 'NA'
        else: wordlist = 'any'

        
        BuildRef.Build_ref_files(tf, rf_std_out, rf_obs_out, wordlist, listuse)
        print "~~~~~~~~~Building Complete~~~~~~~~"
        print "Check: ", rf_std_out, " AND ", rf_obs_out


    #############Create Weighted(u) matrix and Y(u) vector files################
    if mode_arg.lower() == "create_wu_y":
        import CreateWu_Y
        print "Creating Weight and Y vector files"

        try:
            if '-kern' in args:
                fullarg = args[args.index("-kern")+1]
                kerntype = fullarg[:fullarg.rfind('_')]
                print kerntype
                dist = float(fullarg[fullarg.rfind('_')+1:])
                print dist
            else:
                kerntype = 'quartic'
                dist = 900000.0
        except:
            print "Kernel Argument is not formmated correctly"
            print "it should be something like quartic_900000 or epanech_800000 (units must be meters)"
            print "run with -help for more options"
            sys.exit("Error")
        try:
            ulist = (args[args.index("-ulist")+1]).split(',')
        except:
            print "Your ulist is not formatted correctly"
            print "it should be something like 400,8,3000 with no spaces between the numbers"
            sys.exit("Error")

        try:
            ptbl = args[args.index("-ptbl")+1]
        except:
            print "ERROR ON -ptbl argument"
            print "This argument should contain the name of the table which was created using DB_Load"
            sys.exit("Error")

        if '-pointgrid' in args:
            pointgrid = args[args.index("-pointgrid")+1]
        else: pointgrid = 'pointgrid_5_clip'
            
        try:
            conn = args[args.index('-conn')+1]
        except:
            print "Problem parsing the connection information provided"

        if '-zeroed' in args:
            zval = args[args.index('-zeroed')+1]
            if zval.lower() == 'f':
                zeroed = False
            else: zeroed = True
        else: zeroed = True


        rf_obs_in = args[args.index("-rf_obs_in")+1]

        w_y_direct = args[args.index("-wu_y_dir_out")+1]

        CreateWu_Y.create(w_y_direct, ulist, kerntype, dist, conn, ptbl, pointgrid, zeroed, rf_obs_in)

    #################Create and Load Database With People/Documents####################
    if mode_arg.lower() == "db_load":
        import DB_Load
        print "Beginning DB Loading Process"

        if '-tf' in args:
            f = args[args.index("-tf")+1]
        elif '-df' in args:
            f = args[args.index("-df")+1]
        elif '-tstf' in args:
            f = args[args.index("-tstf")+1]

        tbl_name = args[args.index("-ptbl")+1]

        try:
            conn = args[args.index('-conn')+1]
        except:
            print "Problem parsing the connection information provided"


        DB_Load.Load(f, tbl_name, conn)

    #################Train the prediction model on given file using GWR####################
    if mode_arg.lower() == "train":
        import Train
        print "Beginning GWR Train Process"

        if '-tf' in args:
            f = args[args.index("-tf")+1]
        elif '-df' in args:
            f = args[args.index("-df")+1]
        elif '-tstf' in args:
            f = args[args.index("-tstf")+1]

        rf_obs_in = args[args.index("-rf_obs_in")+1]

        rf_std_in = args[args.index("-rf_std_in")+1]

        wu_y_direct = args[args.index("-wu_y_dir_in")+1]

        b_direct = args[args.index("-b_dir_out")+1]

        if '-lam' in args:
            lam = float(args[args.index("-lam")+1])
        else: lam = 0

        try:
            ulist = (args[args.index("-ulist")+1]).split(',')
        except:
            print "Your ulist is not formatted correctly"
            print "it should be something like 400,8,3000 with no spaces between the numbers"
            sys.exit("Error")

        try:
            if '-kern' in args:
                fullarg = args[args.index("-kern")+1]
                kerntype = fullarg[:fullarg.rfind('_')]
                print kerntype
                dist = float(fullarg[fullarg.rfind('_')+1:])
                print dist
            else:
                kerntype = 'quartic'
                dist = 900000.0
        except:
            print "Kernel Argument is not formmated correctly"
            print "it should be something like quartic_900000 or epanech_800000 (units must be meters)"
            print "run with -help for more options"
            sys.exit("Error")

        Train.train(f, rf_obs_in, rf_std_in, wu_y_direct, ulist, kerntype, lam, b_direct)

    if mode_arg.lower() == "test":
        import Test

        if '-tf' in args:
            f = args[args.index("-tf")+1]
        elif '-df' in args:
            f = args[args.index("-df")+1]
        elif '-tstf' in args:
            f = args[args.index("-tstf")+1]

        rf_std_in = args[args.index("-rf_std_in")+1]

        b_direct = args[args.index("-b_dir_in")+1]

        try:
            ulist = (args[args.index("-ulist")+1]).split(',')
        except:
            print "Your ulist is not formatted correctly"
            print "it should be something like 400,8,3000 with no spaces between the numbers"
            sys.exit("Error")
            
        try:
            if '-kern' in args:
                fullarg = args[args.index("-kern")+1]
                kerntype = fullarg[:fullarg.rfind('_')]
                print kerntype
                dist = float(fullarg[fullarg.rfind('_')+1:])
                print dist
            else:
                kerntype = 'quartic'
                dist = 900000.0
        except:
            print "Kernel Argument is not formmated correctly"
            print "it should be something like quartic_900000 or epanech_800000 (units must be meters)"
            print "run with -help for more options"
            sys.exit("Error")

        Test.test(f, rf_std_in, b_direct, ulist, kerntype)
        
        
    #except:
    #    print "ERROR: THERE WAS A PROBLEM INTERPRETING THE ARGUMENTS"
    #    print "Must Specify -mode"
    #    print "Execute GWRMain.py -help  for information"
elif "-help" in sys.argv:
    print "---------------------"
    print "MODE ARGUMENTS"
    print "-mode"
    print "db_load ((-tf OR -df OR -tstf), -conn, -tbl)"
    print "Build_ref_files (-tf, -rf_std_out, -rf_obs_out, -wordlist(OPTIONAL))"
    print "NOT FUNCTIONAL: Create_Wu ((-tf OR -df OR -tstf), -kern, -ulist, -wu_dir_out)"
    print "NOT FUNCTIONAL: Create_Y ((-tf OR -df OR -tstf), -ulist, -y_dir_out)"
    print "Create_Wu_Y (-ptbl, -conn, -pointgrid(OPTIONAL), -kern(OPTIONAL), -zeroed(OPTOINAL), -ulist, -wu_y_dir_out, -rf_obs_in)"
    print "Train (-tf, (-wu_y_dir_in OR (-y_dir_in AND -wu_dir_in), -rf_std_in, -rf_obs_in, -ulist, -b_dir_out, -lambda))"
    print "NOT FUNCTIONAL: Test (-tstf, -rf_std_in, -b_dir_in, -pred_out)"
    print "NOT FUNCTIONAL: Train_Test (-tf, -tstf, (-wu_y_dir_in OR (-y_dir_in AND -wu_dir_in), -rf_std_in, -rf_obs_in, -ulist, -b_dir_out, -pred_out, -lambda))"

    print "---------------------"
    print "Train File"
    print "-tf"
    print "absolute path of train file"

    print "---------------------"
    print "Devel File"
    print "-df"
    print "absolute path of devel file"

    print "---------------------"
    print "Test File"
    print "-tstf"
    print "absolute path of test file"
    
    print "---------------------"
    print "Standard Deviation Reference File (in)"
    print "-rf_std_in"
    print "absolute path of std_dev reference"

    print "---------------------"    
    print "Standard Deviation Reference File (out)"
    print "-rf_std_out"
    print "absolute path of std_dev reference"

    print "---------------------"    
    print "Observation (aka people, users) Reference File (in)"
    print "-rf_obs_in"
    print "absolute path of std_dev reference"

    print "---------------------"    
    print "Observation (aka people, users) Reference File (out)"
    print "-rf_obs_out"
    print "absolute path of std_dev reference" 

    print "---------------------"
    print "Weight Matrix Directory (out)"
    print "-wu_dir_out"

    print "---------------------"
    print "Weight Matrix Directory (in)"
    print "-wu_dir_in"

    print "---------------------"
    print "Y(u) vector Directory (out)"
    print "-y_dir_out"

    print "---------------------"
    print "Y(u) vector Directory (in)"
    print "-y_dir_in"

    print "---------------------"
    print "Weight Matrix and Y(u) vector Directory (out)"
    print "-wu_y_dir_out"

    print "---------------------"
    print "Weight Matrix and Y(u) vector Directory (in)"
    print "-wu_y_dir_in"

    print "---------------------"
    print "Ulist: a list of grid point id's; a different regression is trained for each one"
    print "-ulist"
    print "e.g. -ulist 900,2000,2100,4000,5000"

    print "---------------------"
    print "Score Files (out)"
    print "-b_dir_out"
    print "directory where score files will be written to"

    print "---------------------"
    print "Score Files (in)"
    print "-b_dir_in"
    print "directory where score files will be read from"

    print "---------------------"
    print "lambda (cost value), default set to 1"
    print "-lambda"

    print "---------------------"
    print "Predictions Out"
    print "-pred_out"
    print "Absolute path of a file predictions written to"

    print "---------------------"
    print "Kernel Function (OPTIONAL)(defaults to quartic_900000) (<method>_<number_of_meters>)"
    print "-kern"
    print "e.g. quartic, epanech"

    print "---------------------"
    print "-Zeroed Kernel (OPTIONAL)"
    print "-zeroed"
    print "e.g. -zeroed F"

    print "---------------------"
    print "-Person Table: name of person table that you are creating/reading from in postgres"
    print "-ptbl"
    print "i.e. do not begin with symbols/numbers and avoid upper case"

    print "---------------------"
    print "-Word List File: name of a file that contains words (one per line) that you want to include in the model"
    print "-wordlist"
    print "OPTIONAL: if left unspecified will default to all possible words in the train file"
    print "Should be an absolute path"

    
    
else:
    print "###ERRROR####: You did not specify enough arguments"
    print "Try -help"
