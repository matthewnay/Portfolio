clear 

import delimited "pitchingmaster.csv"

tabulate tm, generate(tm_dummy)

local trad "p_total_hits p_home_run p_strikeout p_walk p_k_percent p_bb_percent	batting_avg	slg_percent	on_base_percent	on_base_plus_slg	p_win	p_loss	p_era" 

local sabr "xba	xslg	woba	xwoba	xobp	xiso	exit_velocity_avg	launch_angle_avg	sweet_spot_percent	barrel_batted_rate"

summarize ln_salary war servicetime nonwhite year `sabr'
summarize `sabr'

encode international, gen(internationaldummy)


// tabstat internationaldummy ln_salary war age servicetime nonwhite year b_total_hits b_home_run b_strikeout b_walk batting_avg slg_percent on_base_percent on_base_plus_slg xba xslg xwoba xobp xiso exit_velocity_avg launch_angle_avg sweet_spot_percent barrel_batted_rate, c(stat) stat(mean sd min max n)
// est clear  // clear the stored estimates
// estpost tabstat internationaldummy ln_salary war age servicetime nonwhite year b_total_hits b_home_run b_strikeout b_walk batting_avg slg_percent on_base_percent on_base_plus_slg xba xslg xwoba xobp xiso exit_velocity_avg launch_angle_avg sweet_spot_percent barrel_batted_rate, c(stat) stat(mean sd min max n)
//
// ereturn list // list the stored locals
//
// // esttab using "summarytable1.tex", replace ////
// //  cells("mean(fmt(%6.2fc)) sd(fmt(%6.2fc)) min max count") nonumber ///
// //   nomtitle nonote noobs label booktabs ///
// //   collabels("Mean" "SD" "Min" "Max" "N")
//  


reg ln_salary war age internationaldummy year
estimates store eq1

reg ln_salary war `trad' age internationaldummy year

reg ln_salary war servicetime internationaldummy year
estimates store eq2

reg ln_salary `trad' servicetime nonwhite year

reg ln_salary war servicetime internationaldummy `sabr'
estimates store eq3

reg ln_salary war servicetime internationaldummy year `sabr'
estimates store eq4

reg ln_salary war servicetime internationaldummy `trad' tm_dummy* if tm_dummy1 != 1
estimates store eq5

reg ln_salary war servicetime internationaldummy `sabr' tm_dummy* if tm_dummy1 != 1
estimates store eq6

reg ln_salary war servicetime internationaldummy `sabr' `trad' tm_dummy* if tm_dummy1 != 1
estimates store eq7

esttab eq1 eq2 eq3 eq4 eq5 eq6 eq7 using "regressionstable4.tex"

ivregress 2sls ln_salary (war = `sabr' `trad') nonwhite servicetime tm_dummy* if tm_dummy1 != 1
