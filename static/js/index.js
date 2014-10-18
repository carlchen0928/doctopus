$(document).ready(function(){
	

$('.subnav ul li a').click(function(){
	if($('.subnav ul li').hasClass('active')){
			$('.subnav ul .active').removeClass('active');
		}
	$(this).parent().addClass('active');
	var htmlid = $(this).attr('id');
	var url = "/urlcrawler/" + htmlid;
	//alert(url);
	$('#load-html').load(url, function(){
		//alert(htmlid);
		//tab切换选项卡
		$('.selctMdl ul li a').click(function(){
			if($('.selctMdl ul li').hasClass('active')){
					$('.selctMdl ul .active').removeClass('active');
				}
			$(this).parent().addClass('active');
			$('.item-mdl .show').removeClass('show');
			$('.'+$(this).attr('id')).addClass('show');
			$('.show input[type=text]').val("");
			$('.show textarea').val("");
		});	
		
		//点击id 进入详情页面
		$('.crawId').click(function(){
			var crawlid = $(this).html();
			$('#load-html').load('crawlDetails.html',function(){
				//alert(crawlid);
				});
			});
	});
	
});

$('#myCrawls').click();
});

