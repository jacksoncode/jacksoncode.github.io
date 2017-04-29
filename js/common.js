/*菜单处于当前状态*/
function leftDropdown(obj){
	var host = window.location.host,
		url = location.href,
		domain = "http://"+host+"/",
		menu = url.replace(domain,"");
	$(obj).each(function(){
		var current = $(this).find("a");
		$(this).removeClass("current");
		if(menu == $(current[0]).attr("href")){
			$(this).addClass("current");
		}
	});
}
$(function(){
	/*新窗口查看代码*/
	$.Huihover('.codeView');
	
	/*返回顶部调用*/
	$(window).on("scroll",backToTopFun);
	backToTopFun();
	
	leftDropdown(".menu_dropdown ul li");
}); 