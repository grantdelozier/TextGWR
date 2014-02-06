import sys


if len(sys.argv) >= 3:
    #try:
    print sys.argv
    args = sys.argv
    mode_arg = args[args.index("-mode")+1]
    print mode_arg
    if mode_arg.lower() == "build_ref_files":
        import BuildRef
        print "Building Reference Files"
        tf = args[args.index("-tf")+1]
        print tf
        rf_std_out = args[args.index("-rf_std_out")+1]
        print rf_std_out
        rf_obs_out = args[args.index("-rf_obs_out")+1]
        print rf_obs_out
        BuildRef.Build_ref_files(tf, rf_std_out, rf_obs_out)
        print "~~~~~~~~~Building Complete~~~~~~~~"
        print "Check: ", rf_std_out, " AND ", rf_obs_out
    if mode.arg.lower() == "create_wu_y":
        import CreateWu_Y
        if '-tf' in args:
            f = args[args.index("-tf")+1]
        elif '-df' in args:
            f = args[args.index("-df")+1]
        elif '-tstf' in args:
            f = args[args.index("-tstf")+1]
        try:
            if '-kern' in args:
                fullarg = args[args.index("-kern")+1]
                kerntype = fullarg[:fullarg.rfind('_')]
                print kerntype
                dist = float(fullarg[fullarg.rfind('_'):])
                print dist
            else:
                kerntype = 'quartic'
                dist = 900000.0
        except:
            print "Kernel Argument is not formmated correctly"
            print "it should be something like quartic_900000 or quartic_zeroed_900000 (units must be meters)"
            print "run with -help for more options"
            sys.exit("Error")
        try:
            ulist = (args[args.index("-ulist")+1]).split(',')
        except:
            print "Your ulist is not formatted correctly"
            print "it should be something like 400,8,3000 with no spaces between the numbers"
            sys.exit("Error")

        try:
            conn - args[args.index('-conn')+1]

        w_y_direct = args[args.index("-wu_y_dir_out")+1]

        CreateWu_Y.create(f, w_y_direct, ulist, kerntype, dist, conn)
            
        
    #except:
    #    print "ERROR: THERE WAS A PROBLEM INTERPRETING THE ARGUMENTS"
    #    print "Must Specify -mode"
    #    print "Execute GWRMain.py -help  for information"
elif "-help" in sys.argv:
    print "---------------------"
    print "MODE ARGUMENTS"
    print "-mode"
    print "Build_ref_files (-tf, -rf_std_out, -rf_obs_out)"
    print "Create_Wu ((-tf OR -df OR -tstf), -kern, -ulist, -wu_dir_out)"
    print "Create_Y ((-tf OR -df OR -tstf), -ulist, -y_dir_out)"
    print "Create_Wu_Y ((-tf OR -df OR -tstf), -kern, -ulist, -wu_y_dir_out)"
    print "Train (-tf, (-wu_y_dir_in OR (-y_dir_in AND -wu_dir_in), -rf_std_in, -rf_obs_in, -ulist, -b_dir_out, -lambda))"
    print "Test (-tstf, -rf_std_in, -b_dir_in, -pred_out)"
    print "Train_Test (-tf, -tstf, (-wu_y_dir_in OR (-y_dir_in AND -wu_dir_in), -rf_std_in, -rf_obs_in, -ulist, -b_dir_out, -pred_out, -lambda))"

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
    print "e.g. quartic, epanech, quartic_zeroed, epanech_zeroed"

    
    
else:
    print "###ERRROR####: You did not specify enough arguments"
    print "Try -help"
