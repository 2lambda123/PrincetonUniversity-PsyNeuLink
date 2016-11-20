Search.setIndex({envversion:50,filenames:["AdaptiveIntegrator","Comparator","ControlMechanism","ControlSignal","DDM","DefaultControlMechanism","EVCMechanism","Function","InputState","LearningSignal","Log","Mapping","Mechanism","MonitoringMechanism","OutputState","ParameterState","Preferences","Process","ProcessingMechanism","Projection","Run","State","System","Transfer","Utilities","WeightedError","index"],objects:{"":{Comparator:[1,0,0,"-"],ControlMechanism:[2,0,0,"-"],ControlSignal:[3,0,0,"-"],DDM:[4,0,0,"-"],DefaultControlMechanism:[5,0,0,"-"],EVCMechanism:[6,0,0,"-"],Function:[7,0,0,"-"],InputState:[8,0,0,"-"],LearningSignal:[9,0,0,"-"],Mapping:[11,0,0,"-"],Mechanism:[12,0,0,"-"],MonitoringMechanism:[13,0,0,"-"],OutputState:[14,0,0,"-"],ParameterState:[15,0,0,"-"],Preferences:[16,0,0,"-"],Process:[17,0,0,"-"],Projection:[19,0,0,"-"],Run:[20,0,0,"-"],State:[21,0,0,"-"],System:[22,0,0,"-"],Transfer:[23,0,0,"-"],WeightedError:[25,0,0,"-"]},"Comparator.Comparator":{"function":[1,2,1,""],comparison_operation:[1,2,1,""],name:[1,2,1,""],outputValue:[1,2,1,""],prefs:[1,2,1,""],sample:[1,2,1,""],target:[1,2,1,""],terminate_function:[1,3,1,""],value:[1,2,1,""],variable:[1,2,1,""]},"ControlMechanism.ControlMechanism_Base":{allocationPolicy:[2,2,1,""],controlSignalCosts:[2,2,1,""],controlSignals:[2,2,1,""]},"ControlSignal.ControlSignal":{"function":[3,2,1,""],adjustmentCost:[3,2,1,""],adjustmentCostFunction:[3,2,1,""],allocation:[3,2,1,""],allocationSamples:[3,2,1,""],cost:[3,2,1,""],costCombinationFunction:[3,2,1,""],durationCost:[3,2,1,""],durationCostFunction:[3,2,1,""],get_costs:[3,3,1,""],intensity:[3,2,1,""],intensityCost:[3,2,1,""],intensityCostFunction:[3,2,1,""],last_allocation:[3,2,1,""],last_intensity:[3,2,1,""],receiver:[3,2,1,""],sender:[3,2,1,""],toggle_cost_function:[3,3,1,""],value:[3,2,1,""]},"DDM.DDM":{"function":[4,2,1,""],function_params:[4,2,1,""],name:[4,2,1,""],outputValue:[4,2,1,""],prefs:[4,2,1,""],terminate_function:[4,3,1,""],value:[4,2,1,""],variable:[4,2,1,""]},"DefaultControlMechanism.ControlSignalChannel":{inputState:[5,2,1,""],outputIndex:[5,2,1,""],outputState:[5,2,1,""],outputValue:[5,2,1,""],variableIndex:[5,2,1,""],variableValue:[5,2,1,""]},"DefaultControlMechanism.DefaultControlMechanism":{Linear:[5,1,1,""],instantiate_control_signal_channel:[5,3,1,""]},"DefaultControlMechanism.DefaultControlMechanism.Linear":{"function":[5,3,1,""],derivative:[5,3,1,""]},"EVCMechanism.EVCMechanism":{"function":[6,2,1,""],EVCmax:[6,2,1,""],EVCmaxPolicy:[6,2,1,""],EVCmaxStateValues:[6,2,1,""],controlSignalSearchSpace:[6,2,1,""],cost_aggregation_function:[6,2,1,""],make_default_controller:[6,2,1,""],monitoredOutputStates:[6,2,1,""],monitoredValues:[6,2,1,""],outcome_aggregation_function:[6,2,1,""],predictionMechanisms:[6,2,1,""],predictionProcesses:[6,2,1,""],prediction_mechanism_params:[6,2,1,""],prediction_mechanism_type:[6,2,1,""],save_all_values_and_policies:[6,2,1,""],system:[6,2,1,""]},"Function.BackPropagation":{"function":[7,3,1,""]},"Function.BogaczEtAl":{"function":[7,3,1,""]},"Function.Contradiction":{"function":[7,3,1,""],Manner:[7,1,1,""]},"Function.Exponential":{"function":[7,3,1,""],derivative:[7,3,1,""]},"Function.Integrator":{"function":[7,3,1,""]},"Function.Linear":{"function":[7,3,1,""],derivative:[7,3,1,""]},"Function.LinearCombination":{"function":[7,3,1,""]},"Function.LinearMatrix":{"function":[7,3,1,""],instantiate_matrix:[7,3,1,""]},"Function.Logistic":{"function":[7,3,1,""],derivative:[7,3,1,""]},"Function.NavarroAndFuss":{"function":[7,3,1,""]},"Function.Reinforcement":{"function":[7,3,1,""]},"Function.SoftMax":{"function":[7,3,1,""],derivative:[7,3,1,""]},"LearningSignal.LearningSignal":{errorSignal:[9,2,1,""],errorSource:[9,2,1,""],mappingProjection:[9,2,1,""],mappingWeightMatrix:[9,2,1,""],receiver:[9,2,1,""],sender:[9,2,1,""],value:[9,2,1,""],variable:[9,2,1,""],weightChangeMatrix:[9,2,1,""]},"Mapping.Mapping":{matrix:[11,2,1,""],monitoringMechanism:[11,2,1,""]},"Mechanism.Mechanism_Base":{execute:[12,3,1,""],function_params:[12,2,1,""],initialize:[12,3,1,""],inputState:[12,2,1,""],inputStates:[12,2,1,""],inputValue:[12,2,1,""],name:[12,2,1,""],outputState:[12,2,1,""],outputStates:[12,2,1,""],outputValue:[12,2,1,""],parameterStates:[12,2,1,""],phaseSpec:[12,2,1,""],prefs:[12,2,1,""],processes:[12,2,1,""],run:[12,3,1,""],systems:[12,2,1,""],timeScale:[12,2,1,""],value:[12,2,1,""],variable:[12,2,1,""]},"MonitoringMechanism.MonitoringMechanism_Base":{monitoredStateChanged:[13,2,1,""]},"Process.Process_Base":{clamp_input:[17,2,1,""],execute:[17,3,1,""],input:[17,2,1,""],inputValue:[17,2,1,""],learning:[17,2,1,""],mechanismNames:[17,2,1,""],monitoringMechanisms:[17,2,1,""],name:[17,2,1,""],numPhases:[17,2,1,""],originMechanisms:[17,2,1,""],outputState:[17,2,1,""],pathway:[17,2,1,""],prefs:[17,2,1,""],processInputStates:[17,2,1,""],results:[17,2,1,""],run:[17,3,1,""],systems:[17,2,1,""],terminalMechanisms:[17,2,1,""],timeScale:[17,2,1,""],value:[17,2,1,""]},"System.System_Base":{InspectOptions:[22,1,1,""],controlMechanisms:[22,2,1,""],execute:[22,3,1,""],executionGraph:[22,2,1,""],executionList:[22,2,1,""],execution_graph_mechs:[22,2,1,""],execution_sets:[22,2,1,""],graph:[22,2,1,""],initial_values:[22,2,1,""],inputValue:[22,2,1,""],inspect:[22,3,1,""],mechanisms:[22,2,1,""],mechanismsDict:[22,2,1,""],monitoringMechanisms:[22,2,1,""],name:[22,2,1,""],numPhases:[22,2,1,""],originMechanisms:[22,2,1,""],processes:[22,2,1,""],results:[22,2,1,""],run:[22,3,1,""],show:[22,3,1,""],terminalMechanisms:[22,2,1,""],timeScale:[22,2,1,""],value:[22,2,1,""]},"Transfer.Transfer":{"function":[23,2,1,""],name:[23,2,1,""],outputValue:[23,2,1,""],prefs:[23,2,1,""],value:[23,2,1,""],variable:[23,2,1,""]},"WeightedError.WeightedError":{name:[25,2,1,""],next_level_projection:[25,2,1,""],outputValue:[25,2,1,""],prefs:[25,2,1,""],value:[25,2,1,""],variable:[25,2,1,""]},Comparator:{Comparator:[1,1,1,""],random:[1,4,1,""]},ControlMechanism:{ControlMechanism_Base:[2,1,1,""]},ControlSignal:{ControlSignal:[3,1,1,""],ControlSignalCostOptions:[3,1,1,""]},DDM:{DDM:[4,1,1,""],DDM_Output:[4,1,1,""]},DefaultControlMechanism:{ControlSignalChannel:[5,1,1,""],DefaultControlMechanism:[5,1,1,""]},EVCMechanism:{EVCMechanism:[6,1,1,""]},Function:{BackPropagation:[7,1,1,""],BogaczEtAl:[7,1,1,""],Contradiction:[7,1,1,""],Exponential:[7,1,1,""],Integrator:[7,1,1,""],Linear:[7,1,1,""],LinearCombination:[7,1,1,""],LinearMatrix:[7,1,1,""],Logistic:[7,1,1,""],NavarroAndFuss:[7,1,1,""],Reinforcement:[7,1,1,""],SoftMax:[7,1,1,""]},LearningSignal:{LearningSignal:[9,1,1,""]},Mapping:{Mapping:[11,1,1,""]},Mechanism:{Mechanism_Base:[12,1,1,""],mechanism:[12,4,1,""]},MonitoringMechanism:{ComparatorOutput:[13,1,1,""],MonitoringMechanism_Base:[13,1,1,""]},Process:{Process_Base:[17,1,1,""],process:[17,4,1,""]},Run:{random:[20,4,1,""],run:[20,4,1,""]},System:{System_Base:[22,1,1,""],system:[22,4,1,""]},Transfer:{Transfer:[23,1,1,""],Transfer_Output:[23,1,1,""]},WeightedError:{WeightedError:[25,1,1,""],WeightedErrorOutput:[25,1,1,""],random:[25,4,1,""]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","attribute","Python attribute"],"3":["py","method","Python method"],"4":["py","function","Python function"]},objtypes:{"0":"py:module","1":"py:class","2":"py:attribute","3":"py:method","4":"py:function"},terms:{"0x10bc59a60":7,"0x10bc83510":[5,7,25],"0x10bca5d90":5,"0x10c63ed68":7,"0x10cc89278":7,"0x10cc893c8":7,"0x10cd184e0":7,"0x10cd18550":7,"0x10cd186d8":7,"0x10cd18a58":7,"0x10cd2c268":7,"0x10cd2c2f0":7,"0x10d6200f0":20,"0x10d620128":20,"0x10d6201d0":20,"0x10d636b00":20,"0x10d636b70":20,"0x10d636be0":20,"0x10d636c50":20,"0x10d636f60":20,"0x10d636fd0":20,"1st":[1,4,23],"2nd":[1,4,7,23],"3rd":[1,4,23],"4th":[1,4],"5th":[1,4],"6th":4,"abstract":[2,12,13,17,22],"boolean":7,"case":[2,3,4,6,8,9,11,12,14,17,20,22],"default":[1,2,3,4],"enum":7,"final":[3,9,17,22],"float":[1,3,4,7,12,23],"function":[1,2,3,4,5,6],"int":[2,12,17,22],"long":[3,8,12,14,23],"new":[2,5,7],"return":[1,3,4,5,7,12,17,20,22,23,25],"true":[3,6,7,17,20,22],"var":7,"while":[12,20,22,26],__execute__:12,__init__:[1,3,4,6,7,8,9,11,12,14,15,17,22,23,25],_control_mech_tupl:22,_controlmechanism_monitored_outputst:6,_instantiate_graph:17,_mechanism_role_in_processes_and_system:6,_monitoring_mech_tupl:22,_phasespecmax:17,_state_creating_a_st:19,_system_execution_control:2,_validate_param:7,abil:[8,14],abl:3,about:[5,12,17,26],abov:[2,3,4,6,11,12,15,17,20,22],absent:[8,12,14,19],absolut:4,accept:[3,8],access:17,accordingli:12,account:9,accumul:[4,7],accumulu:7,accur:7,accuraci:[4,7],achiev:20,across:20,act:26,activ:7,activation_funct:[7,9],actual:17,acycl:22,adapt:3,adaptiveintegratormechan:6,add:[4,5,7,11],addit:[3,4,6,7,11,12,13,19,22,23],addition:3,adher:[19,26],adjac:[11,17,19],adjust:[3,7,25],adjustment_cost_funct:3,adjustment_cost_function:3,adjustmentcost:3,adjustmentcostfunct:3,affect:[20,22],after:[1,4,7,9,11,12,13,17,20,22,23,25],again:17,against:[13,17],aggreg:[6,12,20],aggregr:[12,26],agre:7,algorithm:[7,9,17,25],alia:5,all:[2,3,4,6,7,9,11,12,17,20,22,23],all_output_labels:22,all_output_states:2,all_outputs:22,allcoat:6,alloc:[3,6,19,26],allocation_sampl:3,allocationpolici:2,allocationsampl:[3,6],allow:[19,20,23,26],alon:[2,17,20],along:[11,17],also:[1,2,3,4,8,9,11,12,13,14,17,19,20,22,23,25],altern:[4,7,17],alwai:[1,2,7,11,12,13,17,20,25],ambigu:17,amitai:26,among:[17,20,22,26],analysi:[7,20,22],analyt:[4,7,20],ani:[2,3,4,6,7,8,9,11,12,14,15,17,19,20,22,23,26],anoth:[3,4,11,12,17,19,22,25,26],any:[3,11,12,19,20,22],api:26,appear:[2,17,20,22],append:20,appli:[2,3,7,9,11,17,23],appropri:[3,9,11,12,17,19,20,22],approxim:20,arg:[7,17],argument:[1,2,3,4,5,6,7,8,12,14,15,17,19,20,22,23,25],arithmet:7,arrai:[1,2,3,4,6,7,9,11,12,17,20,22,23,25],array:7,ask:26,assess:[2,6],assgin:6,assign:[1,2,3,4,5,6,8,9,11,12,13,14,15,17,19,20,22,23,25],assigning:5,assignment:9,associ:[2,3,4,6,9,12,15,17,22,25],asssign:4,assum:[2,6,7,8,14],assume:7,attent:4,attribut:[1,2,3,4,5,6,7,9,11,12,17,19,20,22,23,25],attributes:22,augment:5,auto_assign_matrix:11,automat:[1,2,4,6,9,11,12,13,17,19,20,25],automt:12,avail:17,averag:[6,7,23],axi:[11,12,17,20,22],backpropag:[7,9,17,25],ballist:20,base:[2,3,6,7,9,12,13,17,20,22,26],baselin:4,basevalu:12,becaus:[11,20],been:[6,9,11,12,17,20,22,26],befor:[4,7,12,17,20,22,23],begin:22,behavior:[6,17],belong:[1,3,6,8,12,14,17,22],below:[2,3,4,9,11,12,17,19,20,22,23],benefit:6,best:[6,20],between:[6,11,17,19,20,22,25],bia:[7,12,23],bias:7,block:26,blue:12,bogacz:7,bogaczetal:[4,7],bool:[6,13,17,20,22],both:[2,4,8,14,17,20,22,25,26],bound:4,brain:26,branch:17,bring:11,broad:26,brown:[7,12,26],bryn:26,calcul:[1,3,4,5],call:[1,2,4,6,7,8,9,12,13,14,17,19,20,22,23,25],call_after_execut:12,call_after_time_step:[17,20,22],call_after_tri:[17,20,22],call_before_execut:12,call_before_time_step:[17,20,22],call_before_tri:[17,20,22],can:[1,2,3,4,5,6,7,8,9,11,12,13,14,17,19,20,22,23,25,26],cannot:[3,12,17,19],cap:23,carri:12,categori:22,caus:11,ccorrect:4,centralclock:[4,17,20,22],chain:22,chang:[3,7,9,11,13,17],check:17,choic:[4,7],chosen:7,circumst:[11,12,19],clamp:17,clamp_input:17,clariti:[12,15,20],classprefer:[1,3,4,6,9,11,12,17,22,23,25],close:[20,22,26],closest:20,code:26,coeffici:7,coeffienc:7,cognit:26,cohen:[7,26],col0:7,col1:7,col2:7,col3:7,col:7,collect:[6,22],column:[7,9,11,25],combin:[2,3,4,6,7,8,11,12,17,19,20],combinationfunct:[1,6],commit:[20,26],common:20,commonli:[6,8,11,14],comoput:26,comparatormechan:20,comparatoroutput:13,comparison:[1,26],comparison_mean:1,comparison_mse:1,comparison_oper:1,comparison_result:1,comparison_sse:1,comparison_sum:1,compat:[7,8,12,14,15,17,22],compati:17,complet:[4,9],compli:7,compon:[3,4,7,9,12,17,19,26],componentpreferenceset:[17,22],componenttyp:[4,5,12,17,23],compris:6,comput:[2,3,4,6,7,9,25,26],computation:26,concaten:12,concept:20,condit:20,confid:1,configur:[2,6,17],conflict:13,conform:7,connect:[17,19,22],connectionist:[17,26],conribut:11,consist:[7,12,17,20],constant:[7,23],constrain:22,constraint:[5,26],constructor:[1,2,3,4,6,8,9,11,12,13,14,17,19,23,25],contain:[2,3,4,6,7,8,9,11,12,14,15,17,19,20,22,23],context:[1,3,4,5,7,8,11,12,13,14,17,19,22,23,25],contextu:[4,23],continu:[4,17,20],contradict:7,contrarian:7,contribut:[3,6,7,25],control_mechanisms:22,control_projection_receivers:22,control_signal:[12,19],control_signal_params:12,controlallocationpolici:6,controlmechanism_bas:2,controlmechanism_exampl:2,controlmodulatedparamvalu:1,controlsign:2,controlsignal_cost_funct:3,controlsignalchannel:5,controlsignalcost:2,controlsignalcostopt:3,convei:[17,26],conveni:[11,15],convent:[1,3,4,6,9,11,12,17,20,22,23,25],convers:19,convert:[3,7,12,17,19,20],convolv:19,coordin:17,copied:15,core:[12,19,25,26],corpor:26,correct:[4,7,20],correspond:[2,3,4,6,7,8,9,11,12,14,17,19,20,22,23,25],corrrespond:22,cost:[2,3,6],cost_aggregation_funct:6,cost_combination_funct:3,cost_combination_function:3,cost_function_nam:3,costcombinationfunct:3,costs:5,cours:3,created:5,creation:[1,9,13,19,25],criterion:20,curent:3,currenlti:17,current:[2,3,4,7,11,12,17,20,22,23],currentstatetupl:1,custom:[1,3,4,6,9,11,12,23,25],customiz:26,cycle:22,cyclic:22,ddm_creating_a_ddm_mechan:4,ddm_decision_variable:[4,6],ddm_output:4,ddm_probability_lower_threshold:4,ddm_probability_upper_threshold:4,ddm_response_time:4,ddm_rt_correct_mean:4,ddm_rt_correct_variance:4,deal:17,debug:12,decis:[4,7],deep:26,defaul:[4,5,7],default_allocation_samples:3,default_input_valu:[2,4,5,12,17,20,22,23],default_matrix:11,default_projection_matrix:17,default_sample_and_target:1,default_sample_values:3,defaultcontrol:[5,6,22],defaultcontrolalloc:[3,5],defaultcontrolmechan:5,defaultmechan:[12,17,19],defaultprocess:22,defer:9,deferred_init:9,deferred_initialization:3,defin:[1,3,4,5,6,7,9,11,12,14,17,20,22,23,25],delta:[7,9,25],delta_weight:7,depend:[2,3,9,11,19,20,22],deriv:[5,7],describ:[2,3,6,7,9,11,12,17,22],descript:[1,3,4,5,6,7,9,11,12,17,20,22,23,25],design:[2,6,12,17,20,22,26],desir:[2,12,13,17,19,26],destin:11,detail:[1,3,4,6,9,11,12,15,17,19,20,22,23,25],determin:[1,2,3,4,6,7,9,11,12,17,19,20,22],devoid:22,diagon:7,diciontari:22,dict:[1,3,4,5,6,7,8,9,11,12,14,15,17,19,20,22,23,25],dict_output:22,dictionari:[1,2,3,4,6,8,9,11,12,14,15,17,19,20,22,23,25,26],differ:[3,4,6,9,12,17,19,22],differenti:25,diffus:[4,7],dimens:[7,11,20],dimension:20,direct:[2,12,13,17,22],directi:20,directli:[1,4,8,12,14,17,19,20,23,25],disabl:[3,17,20,22],disagre:7,discount:6,discuss:[20,22],dispar:[9,26],dissemin:26,distribut:[4,7,11],divid:[1,6],divis:1,division:1,divisor:6,document:[7,12,19],documentation:5,doe:[2,9,17,19,22,26],does:5,don:22,done:[1,2,6,8,9,12,14,20],downstream:19,drawn:[4,11],dreceiv:7,drift:[4,12],drift_rat:[4,7],drift_rate:[4,7],dsender:7,due:11,duplic:[1,3,4,6,9,11,12,17,22,23,25],durat:1,duration_cost_funct:3,duration_cost_function:3,durationcost:3,durationcostfunct:3,dure:[3,11,12,17,19,20,22],each:[1,2,3,4,5,6,7,8,9,11,12,13,14,15,17,19,20,22,23,25],easi:26,easier:20,edg:22,effect:[4,9,11,17,22,23],either:[1,2,3,4,7,8,9,12,15,17,19,20,22,23,25,26],element:[1,3,4,7,11,12,20,23,25],elementwis:12,elig:17,elsewher:7,emb:20,emergent:26,emo:14,emp:15,empti:22,emv:[8,14],enabl:[3,17,20,22],enable_control:22,encourag:26,engin:4,enrti:8,enter:17,entir:[7,17],entri:[1,2,3,4,5,6,7,8,9,11,12,14,15,17,19,20,22,23,25],enumer:[3,4,7,13,23,25],environ:26,equal:[3,4,6,7,11,12,17,20,22],equival:6,equivoc:7,error:[1,4,7,9,11,12,13,17,19],error_arrai:25,error_sign:25,error_sourc:[7,9,25],errorsign:9,errorsourc:9,esp:22,estim:4,etc:[4,5,12,23],evalu:[6,11,12,13,17,26],evaluat:11,evc:[2,3,5],evc_mechanism_exampl:6,evcmax:6,evcmaxpolici:6,evcmaxstatevalu:6,evcmechan:2,evcmechanism_parameterizing_evc_objective_funct:6,even:[2,4,17,20],ever:20,everi:[4,6,12,17,20,22,26],every:5,exactli:[7,12],examin:26,exampl:[4,6,7,11,12,13,17,19,20,22,23],example:4,except:[2,3,8,14,20],exclud:[2,9,17],exece:23,execute:5,execution_graph_mech:22,execution_set:22,execution_sets:22,executiongraph:22,executionlist:[20,22],exist:[12,17,19,22],expect:[4,6,12,19],explain:5,explan:[2,3,9,12,17],explicilti:17,explicitli:[4,17],expon:[2,6,7],exponenti:[2,3,7,23],exponents:7,express:26,extend:26,extens:26,extrem:20,factor:[7,12,20],factori:[12,17,22],failur:9,fall:22,fals:[6,7,17,20,22],familiar:26,fashion:11,fast:7,faster:23,feedback:[17,22],few:[20,26],field:5,figur:[9,12,17,20,25],fill:[7,11],filler:7,filter:7,first:[1,2,3,4,6,7,8,11,12,14,15,17,20,22,23],flat_output:22,flexibl:[11,26],follow:[1,2,4,6,7,8,11,12,14,15,17,19,20,22,23,25,26],forc:[4,7,17,20,22],form:[6,12,17,19,20,26],formal:7,format:[6,7,11,12,17,20,22,26],forth:20,four:[3,20],framework:[7,20],from:[1,2,3,4,6,7,8,9,11,12,14,15,17,19,22,25,26],fuction:22,full:[9,12],full_connectivity_matrix:[11,17],fulli:[9,20,22],function__params:12,function_param:[4,12,23],function_params:[4,8,12,14,15,17],functon_params:12,fundament:12,further:[4,12,20],fuss:7,futur:25,gain:[7,12,23],gatingsign:26,gaussian:[4,23],gener:[6,7,9,11,12,13,17,19,20,25,26],get:19,get_cost:3,get_matrix:7,given:[6,11,12,17,20],goal:26,govern:6,granular:[7,26],graph:20,greater:4,green:12,hadamard:[7,11,12],handl:[4,7,12,20],hard_clamp:17,has:5,have:[2,4,6,7,8,9,11,12,14,17,20,22,23,26],height:7,help:20,here:[6,19],hierarch:[4,22,23],higher:[20,23],histori:6,holm:7,how:[1,2,3,4,6,7,9,11,12,17,20,26],howev:[6,9,12,17,19,20,22],ident:[3,7],identifi:13,identity_matrix:[11,17],ignor:[17,20,22,23],impact:[12,22],implement:[1,3,4,5,6,7,9,11,12,17,20,23,25,26],implementation:[1,4,17],impos:[19,26],inccorrect:4,includ:[1,3,4,6,7,9,11,12,17,22,23,25],include:25,increment:[7,8,14],independ:4,index:[1,3,4,6,7,9,11,12,17,22,23,25,26],indic:[7,12,17],indices:7,individu:[7,11,26],induc:17,infer:[8,14,19],influenc:[11,12],inform:[17,19,22,26],iniializ:7,init:7,initalize_cycle:22,initi:[3,7,9,12,17,20,22],initial:[5,7,8,14],initial_cycle:22,initial_valu:[17,20,22,23],initializaton:9,initialize_cycle:[20,22],initializing:[3,4,5,7,23],inlin:[12,17],inline:17,inner:[7,11,20],input:[1,2,3,4,5,6,7],input_array:22,input_state_params:12,input_states:[8,12],inputst:[1,2,5,6,8,9,11,12,14,17,19,20,25],inputstat:1,inputvalu:[7,12,17,22],insid:20,insight:26,inspect:[11,22],inspectionopt:22,inspectoption:22,instal:4,instanc:[6,12,17,19,22,23],instantan:7,instanti:[2,4,5,6,8,12,13,14,15,17,19,22,23],instantiat:[5,15,19],instantiate_control_signal_channel:5,instantiate_matrix:7,instantiate_st:[8,14],institut:26,insur:20,intact:[17,20,22],integr:[3,4,7,26],integratorfunct:[3,4],intel:26,intens:3,intensiti:3,intensity_cost_funct:3,intensitycost:3,intensitycostfunct:3,intenstity_cost_function:3,interact:26,intercept:[3,5,7,12],interfac:26,intern:[12,17,20],internal:22,interpos:17,interv:[1,20,23,25],intial_valu:20,intregr:3,invok:20,involv:[9,17],irrespect:[2,17],is_numerical_or_non:7,is_pref_set:[5,7,25],item:[1,2,4,6,7,8,11,12,13,14,15,17,20,22,23],iter:20,its:5,itself:[9,11,12,17],johnson:26,jonathan:26,journal:7,just:7,keeps:5,kei:[4,6,8,9,12,14,15,17,19,20,22,23],keller:26,kewyord:1,keyword:[1,3,4,6,7,9,11,12,17,19,20,22,23,25],know:[4,5],known:9,kwddm_bia:7,kwfillervalu:7,kwidentiti:7,kwinitial:7,kwinputstat:8,kwinputstatevalu:5,kwkwidentitymap:7,kwlinearcombinationiniti:7,kwmax:7,kwoutputstatevalu:5,kwpertinac:7,kwpredictionmechan:6,kwpropens:7,kwreceiv:7,kwtransferfctderiv:7,kwtransferfunctionderiv:7,kwweight:7,lab:26,label:[12,22],lambda:12,last:[2,3,6,13,17,20],last_alloc:3,last_intens:3,latter:[4,6,12,20],layer:17,lazi:[2,3,9,11,17],lazy_evalu:[2,3,9,17,19],learn:[1,7,9,11,12,13],learning_projection_receivers:22,learning_r:[7,9],learning_rate:7,learning_signal:19,learningsign:[1,7],learningsignal_automatic_cr:[1,19,25],least:[12,17,20,25],left:[17,20,22],len:7,length:[1,4,6,7,8,11,12,14,17,20,22,23,25],level:[12,17,20,22],like:[12,20,26],linear:[2,3,4,5,7,12,23],linearcombin:[1,6,7,11,12],linearli:7,linearmatrix:[7,11],linguist:26,link:[1,3,4,6,9,11,12,13,17,19,20,22,23,25,26],list:[1,2,3,4,6,7,8,9,11,12,14,15,17,19,20,22,23,26],logist:[7,9,12,17,23],loop:[17,20,22],lower:[4,23],lowest:[17,20,22],made:[4,6,9,12,17,25],mai:[2,12,13,17],make:[3,4,6,7,11,17],make_default_control:6,manag:[2,20,26],mani:12,manner:[7,22,26],map:[1,2,5,6,7,9],mapping_params:12,mapping_projection:19,mapping_structur:11,mappingproject:9,mappingweightmatrix:9,match:[7,8,9,14,17,20,25],math:26,mathemat:[7,23],matlab:[4,26],matrix:[7,9,11,17,19,25,26],matrix_spec:7,mattrix:17,max:[6,7,23],max_indicator:7,max_val:7,maxim:6,maximum:[6,7,22,23],may:5,mean:[1,2,4,7,9,12,15,19,23],meant:26,mech:22,mech_spec:[1,4,12,23,25],mech_tupl:22,mechahn:12,mechainsm:12,mechan:1,mechanim:[17,20],mechanism:5,mechanism_1:17,mechanism_2:17,mechanism_3:17,mechanism_bas:12,mechanism_creating_a_mechan:[12,17],mechanism_specifying_paramet:12,mechanism_type:12,mechanismlist:[17,22],mechanismnam:17,mechanismregistri:[1,4,6,12,23,25],mechanisms:22,mechanismsdict:22,mechanismtupl:17,mechansim:9,mechansim_1:17,member:17,mention:12,meshgrid:6,messag:17,met:20,method:[1,2,3,4,5,6,7,8,9,12,13,14,15,17,19,20,22,23],michael:26,might:2,millisecond:4,min:23,mind:[20,26],minimum:[23,26],miss:17,mode:[4,7,20,22],model:[4,7,26],modifi:[3,9,12,17,19,22,25,26],modul:[12,17,19,22,26],modular:26,modulationoper:[11,15],moehli:7,monitor:1,monitor_for_control:[2,6,12,22],monitor_for_learning:[9,12],monitored_output_labels:22,monitored_outputs:22,monitored_states_argu:6,monitoredoutputst:[2,6,11],monitoredoutputstateopt:6,monitoredoutputstatesopt:[2,6],monitoredstatechang:13,monitoredvalu:6,monitoring:22,monitoring_mechanisms:22,monitoringmechan:[1,9,11,12],monitoringmechanism_bas:13,monitoringmechanisms_monitored_for_learn:12,more:[1,2,5,6,7,8,9,11,12,13,14,17,20,22,25,26],most:[11,20],much:20,multi:[8,14],multipl:[4,7,12,17,20],multipli:[2,4,6,7],musslick:26,must:[1,2,3,4,6,7,8,9,11,12,14,15,17,19,20,22,23,25],my_ddm:4,my_linear_transfer_mechan:23,my_logistic_transfer_mechan:23,my_mechan:12,my_process:17,mydecisionprocess:6,myrewardprocess:6,mysystem:6,name:[1,2,3,4,5,6,8,9,11,12,13,14,15,17,19,22,23,25],namedtupl:[12,17],nate:26,natur:9,navarro:7,navarroandfuss:[4,7],ndarrai:[4,7,11,12,17,20,22,23],necessari:[8,9,14,26],necessarili:[12,17,22],need:[5,17,19],needed:5,neg:4,neither:4,nest:[17,20,22],network:17,neural:26,neurosci:26,neuroscientist:26,never:[2,12,13,17,22],nevertheless:20,new_valu:7,newli:2,next:[2,3,4,6,9,17,20,22,25],next_level_project:25,next_level_projection:25,node:22,nois:[7,23],noise:[4,7,17],non:[7,12],non_decision_time:[4,7],none:[1,2,3,4,5,6,7,9,11,12,13,17,19,20,22,23,25],nor:4,normal:4,notat:15,note:[4,6,7,8,12,14,17,19,20,22],notimplement:[5,7,13,17],nparrai:6,nth:[12,17],num_execut:[12,17,20,22],num_phases_per_trial:22,number:[2,4,5,6,7,8,11,12,14,15,17,20,22,25],numer:[4,7,12,20,23],numphas:[17,22],object:[2,7,8,12,14,15,17,19,20,22,26],obsequi:7,obsequious:7,obstin:7,occupi:22,occur:[6,9,11,19,22],ode:26,off:[3,17,20,22],offer:12,offset:[6,7,11],often:4,old:7,old_valu:7,oldvalu:7,omit:17,onc:[12,17,20],once:6,one:[1,9,13,25],onli:[2,4,6,7,8,11,12,14,17,19,20,22,23],only:2,open:26,oper:[1,3,6,7,9,11,26],operat:7,operation:7,opposit:7,optim:[4,6,7],optimiz:6,option:[4,6,7,12,17,20,22],optiona:3,optional:[1,3,4,6,9,11,12,17,23,25],order:[2,3,17,20],ordereddict:[8,12,14,22],orderli:22,ordinarili:19,organ:[22,26],orient:26,origin:[4,6,9,12,17,20,22],origin_mechanisms:22,originmechan:[17,22],other:[2,3,4,6,7,9,11,12,13,17,19,20,22,25,26],otherwis:[2,3,4,6,8,11,12,14,17,19,20],ouptput:19,ouptut:19,ouput:12,ouputst:[2,5],out:12,outcom:[2,4,6,12],outcome_aggregation_funct:6,outcome_aggregation_function:6,outer:[7,11],outermost:[12,17,20,22],output:[1,3,4,5,7,8,9,11,12],output_state_names:22,output_state_params:12,output_states:[12,14],output_type:7,output_value_arrai:22,output_value_array:22,outputindex:5,outputst:1,outputstate:5,outputvalu:[1,4,5,12,22,23,25],outsid:22,outstat:2,over:[2,6,12,17],overrid:[2,4,7,12,17,22],overridden:[1,2,4,12,19],overrides:5,own:[2,4,6,8,12,14,17],owner:[2,3,8,9,14,19],page:26,pair:[6,7,17],parallel:[4,7],param:[1,2,3,4,5,6,7,8,9,11,12,13,14,15,17,22,23,25,26],param_1:12,param_2:12,param_3:12,param_modulation_oper:11,paramclassdefault:[5,8,14,19],paramet:[1,2,3],parameter_modulation_oper:[11,15],parameter_spec:[5,7],parameter_state_params:[12,17],parameter_states:15,parameterst:[3,4,6,9,11],paramscurr:[8,14],paramt:12,paramvalueproject:[8,12,15],parm:[1,3,4,6,9,11,12,23,25],parmaterst:3,pars:20,part:[3,6,9,12,17],particular:[2,6,12,17,19,26],pass:[5,6,7,12,19,22],passag:[4,7],path:[4,22],pathwai:[9,11,12],pathway:17,pattern:17,per:[4,20],perform:[6,7,12,26],perman:3,permiss:22,permit:22,permut:6,pertain:2,pertinac:7,peter:26,phase:[12,17],phasespec:[12,20],physic:7,pick:[6,7],place:[2,6,8,14,17,25],plai:[12,22],plausibl:26,plot:[5,7],point:[8,14,22],polici:6,popul:7,portfolio:6,posit:[4,22],possibl:[6,9,20,26],potenti:26,power:26,preced:[2,12,17],predict:6,prediction_mechanism:6,prediction_mechanism_param:6,prediction_mechanism_typ:6,predictionmechan:6,predictionprocess:6,pref:[1,2,3,4,5,6,7,9,11,12,13,17,22,23,25],preferenceset:[1,3,4,6,9,11,12,17,22,23,25],present:[11,17,20],preserv:17,previou:[3,6,7,11,12,23],primari:[1,2,4,6,9,11,12,17,20,23,25,26],primarili:17,primary_output_labels:22,primary_output_states:[2,6],primary_outputs:22,princeton:26,principl:[19,26],print:22,prior:20,prob:7,probabilisti:7,probability_lower_threshold:4,probability_upper_threshold:4,probabl:4,probe:7,procedur:[4,6],process:[1,2,3,4,6,7,9,11],process_bas:17,process_spec:17,processes:22,processingmechan:[1,2,3,6,9,11,12,13,17,19,22,25],processinputst:17,processregistri:17,product:[4,6,7,12,26],program:26,project:[1,2],projection:5,projection_a:17,projection_bas:19,projection_params:[12,19],projection_sender:19,projection_type:19,projectionregistri:[3,9,11],projections:5,projectiontyp:15,propens:7,provid:[1,3,4,7,8,9,11,12,14,17,20,22,23,26],prune:22,psycholog:[7,26],psyneulink:[4,6,9,11,12,17,19,20,22],psyneulnk:12,purpl:12,purpos:[12,19,20,26],python:[2,6,12,13,19],rais:[8,14],random:[1,4,11,17,20,22,25],random_connectivity_matrix:[11,17],random_matrix:11,rang:[3,11,23],rate:[4,7,12,23],rather:[4,17],ratio:[4,6],reach:4,read:22,real:[20,22],rec0:7,rec1:7,rec2:7,rec3:7,receiv:[1,2,3,4,7,9,11,12,17],receivesfromproject:[12,19],reciev:2,recurr:[17,22],recurrent_init_array:22,recurrent_mechanisms:22,recurrentinitmechan:22,red:12,reduc:[3,9,25],ref:[1,2,4,8,11,12,15,19,25],referenc:22,reflect:26,refs:[4,25],regist:12,registri:[1,3,4,6,9,11,12,17,22,23,25],regul:[2,6],reinforc:[7,17],rel:7,relabeled:15,relev:[9,12,14,17,20,23],remain:[17,22],remov:22,report:[4,7],repres:[12,17,22],represent:26,requir:[4,9,11,12,13,17,20,22],reset:[7,17,20,22],reset_clock:[17,20,22],resolv:7,resolve:23,respect:[6,12,22],respons:[2,3,4,7,12,20],response_time:[4,6],restor:4,result:[1,3,4,5,6,7,8,11,12,14,17,19,20,22,23,26],review:7,reward:6,round:[2,6,17,20,22],rouund:20,row0:7,row1:7,row:[7,9,11,25],rt_correct_mean:4,rt_correct_variance:4,rtype:1,rule:[7,9,25],rumelhart:9,run:[1,4,6,9,12,17],runtim:[4,7],runtime_param:[7,12,17],same:[1,2,4,6,7,9,11,12,15,17,19,20,22,23],sampl:[1,3,4,6,12,22,23],sample:[1,9],sample_input:20,save:6,save_all_values_and_polici:6,scalar:[3,4,5,6,7,20,23,26],scale:[4,6,7,17,20,23,25,26],scaled:7,schemat:12,scienc:26,scope:20,seamless:26,search:26,sebastian:26,second:[1,4,6,7,11,12,15,17,23],see:[1,2,3,4,6,7,8,9,11,12,13,14,15,17,19,20,22,23,25],seek:6,select:[3,4,6,12],self:[6,7,8,12,14,17,22],send:[17,22],sender:[3,5,7,9,11,12,17],senders:5,sendstoproject:19,sendtoproject:6,separ:4,sequenc:[12,17,20,22],sequenti:4,sequeunc:20,seri:17,serv:[1,4,9,12,19,23],set:[3,4,6,7,12,17,20,22,23,26],sever:[12,19,22],shape:7,share:[12,26],shenhav:[6,26],should:[2,3,4,5,12,13,15,17,19,20,22,23],show:[6,11,12,20,22],shown:[6,9,12,25],shvartsman:26,sigmoid:[5,7],signal:2,signmoid:7,similar:12,similarli:12,simpl:[7,23],simpler:20,simplest:[12,19,20],simpli:[4,5,7,12,20,22,23,26],simply:5,simul:[6,26],sinc:[4,13,22],singl:[4,5,6,7,8,12,14,17,20,22,23,25],singleton:22,sit:9,size:[11,20],slope:[3,5,7,12],soft_clamp:17,softmax:[5,7],sole:[8,14],solut:[4,7],some:[12,13,17,19,20,22,26],some_param:17,somefunct:12,somemechan:12,something:5,sophisticated:5,sort:22,sourc:[3,5,9,11,17,19,20,25,26],spec:17,special:[8,12,14],specif:[1,2,3,4,6,7,8,9,11,12,13,14,15,17,19,20,22,23,25],specifi:[1,2,3,4,5,6,7,8,9,11],specifii:12,speicfi:11,sprt:4,squar:[1,11],stand:[17,20],standalon:9,standard:[2,4,6,12,13,19,23,26],start:[4,17,22,23],starting_point:[4,7],state:[1,2,5],state_creating_a_st:19,state_projections:[8,15],statement:7,states:5,statist:4,step:[3,4,12,17,20,22],stepwis:4,still:17,stimulu:4,stimuul:4,stochast:[4,23],stop:4,store:[3,6,7,9,12,17,20,22],str:[1,3,4,5,6,7,8,9,11,12,14,17,22,23,25],stream:9,strength:4,string:[1,2,3,4,6,9,11,12,17,19,22,23],sub:[7,12],subclass:[1,2,4,5,8,12,13,14,15,19,23,25,26],sublist:20,submit:12,subsequ:[4,17],subset:22,subsystem:26,subtract:[1,6],subtraction:1,suffix:[12,17],suitabl:19,sum:[1,3,6,7,12],superced:2,support:[8,12,14,17,20,22],suppress:2,sybmol:26,synonym:12,system:[1,2,3,5,6,9],system_bas:22,system_phas:[12,17],systemdefaultcontrolmechan:22,systemregistri:22,tafc:4,take:[2,3,9,12,13,17,19,22,26],taken:4,target:[1,9,12,17],target_input:20,task:[3,7],tbi:22,tc_predic:7,teano:26,ted:26,templat:[1,4,7,12,17,23,26],tempor:7,tend:7,tendenc:7,tensorflow:26,teriminal:17,term:[7,20],termin:[1,4],terminal:[1,2,6,9,12,17,20,22],terminal_mechanisms:22,terminalmechan:[17,22],terminate_funct:[1,4],test:[4,6,12],than:[2,4,7,8,11,12,14,17,20],thei:[2,4,6,7,11,12,13,17,19,22,23,26],them:[7,8,17,26],themselv:[12,17,22],theoret:22,theori:[6,26],therefor:17,thess:19,thi:[1,2,3,4,6,8,9,11,12,13,15,17,19,20,22,23,25,26],think:26,third:[6,12,17],those:[2,5,6,8,9,11,12,14,17,20,22,23,26],though:17,thought:[4,6],three:[2,3,4,6,7,12,17,19,22],threshold:[4,7,17],through:[7,17,22,26],throughout:17,thu:[2,12],time:[3,4,7,9,12,17],time_averaged:7,time_scal:[4,5,7,12,17,20,22,23],time_step:[4,12,17,20,22,23],times_scal:4,timescal:[4,5,7,12,17,20,22,23],togeth:[22,26],toggl:3,toggle_cost_funct:3,tool:[22,26],tools0:26,topolog:22,toposort:22,total:3,track:5,train:[12,17,26],transfer:[3,6,7,9,11,12,17,18],transfer_default_bias:23,transfer_mean:23,transfer_output:23,transfer_result:23,transfer_variance:23,transferfunct:[3,23],transferfunt:3,transform:[5,7,11,12,17,22,23,26],transmit:[11,12,17,19],treat:2,treatment:20,trial:[4,5,6,7,12,17,20,22,23],ttimescal:4,tupl:[2,6,9,11,12,15,17,19,23],turn:[3,12],two:[1,3,4,6,7,11,12,17,19,20,22,25],type:[1,2,3,7,9,11,12,13,17,19,20,22,23],typecheck:[7,20],typic:[12,19,20,25],unchang:5,under:[1,3,4,6,9,11,12,17,19,22,23,25],understand:20,uniform:11,uniformli:11,unit:[7,9],univers:26,unless:2,until:[2,3,9,11,12,17],updat:[2,3,9,11,12,17,19,20],update:12,upon:20,upper:[4,23],usabl:26,use:[5,7,17],used:[11,19,22],user:26,usual:[3,12,19,20],usualli:12,valid:[7,20],valu:[1,2,3,4,5,6,7,8,9,11,12,13,14,15,17,19],value:23,vari:26,variabl:[1,3,4,5,7,8,9,11,12,13,14,15,17,19,20,23,25,26],variable_default:[5,7],variableclassdefault:7,variableindex:5,variableinstancedefault:[12,17],variablevalu:5,varianc:[4,7,12,23],variou:[12,26],vector:[7,20,26],version:4,wai:[2,3,9,11,12,17,19,22,26],weight:[2,6,7,9,11,13],weightchangematrix:9,weighted_error:25,weightederror:[9,13],weightederroroutput:25,weighting:7,weights:7,well:12,what:[5,26],whatev:19,when:[1,2,4,6,8,9,11,12,13,14,17,19,20,22,23,25],whenev:[2,17,22],where:[6,9,12,19,22],wherev:[2,12],whether:[2,4,6,7,12,13,17,19,20,22,23],which:[1,2,3,4,6,7,8,9,11,12,13,14,17,19,20,22,23,25,26],whose:22,width:[7,25],wiener:[4,7],willk:26,wilson:26,wise:[4,7,11,23],within:[11,17,20,22],without:[9,11,26],word:11,would:[2,20],xxx:12,xxxx:25,yet:26,zero:[4,7,17,22,23]},titles:["Adaptive Integrator","Comparator","Control Mechanisms","Control Signal","DDM","Default Control Mechanism","EVC Mechanism","Functions","Input State","LearningSignal","Log","Mapping","Mechanisms","Monitoring Mechanisms","Output State","Parameter State","Preferences","Process","Processing Mechanisms","Projections","Run","States","System","Transfer","Functions","Weighted Error","PsyNeuLink Documentation"],titleterms:{"class":[1,2,3,4,6,9,11,12,13,17,22,23,25],"default":5,"function":[7,8,12,24,26],adaptiv:0,architectur:26,calcul:6,compar:1,construct:6,contributor:26,control:[2,3,5,22],controlmechan:2,controlsign:3,controlsignalsearchspac:6,creat:[1,2,3,4,6,8,9,11,12,13,14,15,17,19,22,23,25],ddm:4,document:26,entry:10,error:25,evc:6,evcmechan:6,execut:[1,2,3,4,6,9,11,12,13,17,19,22,23,25],graph:22,indice:26,initial:[20,22],input:[8,17,20,22],inputstat:[8,12],integrat:0,learn:[17,22],learningsign:9,log:10,map:11,mechan:[2,4,5,6,12,13,17,18,22,23],monitor:[2,13],monitoringmechan:13,order:22,output:[14,17],outputst:[2,12,14],overview:[1,2,3,4,6,8,9,11,12,13,15,17,19,20,22,23,25,26],paramet:[4,6,12,15],parameter:6,parameterst:[12,15],pathwai:17,phase:22,prefer:16,process:[12,17,18],project:[3,9,11,17,19],psyneulink:26,receiv:19,refer:[1,2,3,4,6,9,11,12,13,17,22,23,25],role:12,run:20,runtim:12,sender:19,signal:3,specifi:12,state:[8,12,14,15,21],structur:[1,3,9,11,12,17,19,22,25],system:[12,22],tabl:26,target:20,time:20,transfer:23,valu:20,weight:25,weightederror:25}})