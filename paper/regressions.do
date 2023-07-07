clear 

import delimited "battingmaster.csv"

tabulate tm, generate(tm_dummy)

summarize ln_salary war servicetime nonwhite year `sabr'
summarize `sabr'

reg ln_salary war age nonwhite year

reg ln_salary war servicetime nonwhite year

local sabr "xba xslg xwoba xobp xiso exit_velocity_avg launch_angle_avg sweet_spot_percent barrel_batted_rate"

reg ln_salary war servicetime nonwhite year `sabr'

reg ln_salary war servicetime nonwhite year `sabr' tm_dummy*

ivregress 2sls ln_salary (servicetime = age nonwhite war) nonwhite war