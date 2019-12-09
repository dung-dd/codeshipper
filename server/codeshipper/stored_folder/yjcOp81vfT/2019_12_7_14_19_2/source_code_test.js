c = {
    "_id" : "f4L5NtfgcJz47AanF",
    "type" : "fb_message",
    "PSID" : "2131700600205509",
    "pageId" : "405864673168997",
    "service_id" : "bTnhbgwSJ2JdpNmfN",
    "created_time" : new Date("2019-07-02T13:11:38.739Z"),
    "latest_updated" : new Date("2019-07-19T08:15:49.169Z"),
    "unread" : 0,
    "active" : true,
    "supporters" : [ 
        {
            "id" : "owMDJN2AixCDeLoAK"
        }
    ],
    "prefix" : "WhLDiO",
    "insert_by" : "webhook",
    "social_account_id" : "gxsEDHYeyMTz9tsCX",
    "name" : "Dũng Bùi",
    "realname" : "Dũng Bùi",
    "email" : "429526450820310@facebook.com",
    "ASID" : "429526450820310",
    "done" : false,
    "seen" : [],
    "snippet" : {
        "icon" : "sending",
        "message" : "lalalala"
    },
    "take_care" : [],
    "take_care_verbose" : new Date("2019-07-19T08:21:49.121Z"),
    "update_by" : "webhook",
    "link" : "/Test-social-listening-tool-405864673168997/inbox/415468938875237/",
    "threadId" : "t_423669758072646",
    "assignment" : {
        "_id" : "owMDJN2AixCDeLoAK",
        "assign_by" : "7b7JKSrfmbyBvWb5G",
        "assign_time" : new Date("2019-07-22T13:11:57.543Z")
    },
    "last_supporter" : "owMDJN2AixCDeLoAK"
}
var time_now = new Date();
var isPassDistributed = false;
var returnState = 0;
var returnMessage = "Cuộc trò chuyện này đã có người chăm sóc.";
var userId = "owMDJN2AixCDeLoAK";
if (c["assignment"] && c["assignment"]["_id"]){
	if (c["assignment"]["_id"] == userId){
		let assign_time = c["assignment"]["assign_time"];
		if ( !assign_time || (time_now < new Date(assign_time) ) ){
			isPassDistributed = true;
			returnState = 1;
			returnMessage = "";
		}
	}
}

console.log(isPassDistributed)