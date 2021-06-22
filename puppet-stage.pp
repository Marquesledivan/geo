 1 #####################
 2 # 1) Define the stages
 3 #####################
 4 
 5 stage { 'prereqs':
 6  before => Stage['main'],
 7 }
 8 
 9 stage { 'final':
10  require => Stage['main'],
11 }
12 
13 #####################
14 # 2) Define the classes
15 #####################
16 
17 # We don't care when this class is executed, it will
18 # be included at random in the main stage
19 class doThisWhenever1 {
20 
21 }
22 
23 # We don't care when this class is executed either, it will
24 # be included at random in the main stage
25 class doThisWhenever2 {
26 
27 }
28 
29 # We want this class to be executed before the
30 # main stage
31 class doThisFirst {
32 
33    exec {'firstThingsFirst':
34      command => '/bin/echo firstThingsFirst',
35    }
36 }
37 
38 # We want this class to be executed after the
39 # main stage
40 class doThisLast {
41 
42   exec {'lastly':
43      command => '/bin/echo lastly',
44    }
45 
46 }
47 
48 #####################
49 # 3) Assign the classes 
50 # to a stage
51 #####################
52 
53 class { 'doThisFirst': 
54   stage => prereqs,
55 }
56 
57 class { 'doThisLast':
58  stage => final,
59 }
60 
61 
62 include doThisFirst
63 include doThisLast   
