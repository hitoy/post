jQuery�ڲ�ԭ��ǳ��
���ʱ����ѧϰ�о�jQueryԴ�룬������jQuery���淢չǿ���о�jQuery�Ĵ�ţԽ��Խ�࣬ѧϰ������Ҳ��ǰ��������ˣ��кܶ�ǳ��������Դ������Ƶ�jQuery1.6.1Դ�����ϵ�У�http://www.cnblogs.com/nuysoft/archive/2011/11/14/2248023.html������Щ�̷̳ǳ�ϸ�µķ�����jQuery�ڲ�ԭ���ʵ�ַ�ʽ����ѧϰ�����jQuery�зǳ���İ��������Ǹ�����Ϊ�ܶ�̶̳�jQuery�����������ղ��㣬������ͼ������������һ��jQuery���ڲ�ʵ�֡�

���֪��������jQuery�����ַ�ʽ��һ���Ǹ߼���ʵ�֣�ͨ������һ������ʵ��DOMѡ����ͨ��$("h1")ѡ�����е�h1Ԫ�أ��ڶ����ǽ�Ϊ�ͼ���ʵ�֣����ͨ��$.ajaxʵ��ajax�Ĳ�������ô�������ַ�ʽ�����кβ�ͬ����typeof�������$('h1')��$.ajax,���ͷֱ�Ϊobject��function����΢ѧ��jQuery�Ķ�֪��������������ǰ�߷��ص���һ��jQuery������ôjQuery������ʲô������jQuery��ʲô��ϵ�أ���������ͨ��for
(var i in $('')) document.write(i+"  :::
"+$("")[i]+"<br/>");��ӡһ��jQuery��������ԺͶ�Ӧ��ֵ,���Կ�������100������ԣ�ͨ��console����$("*")���Կ����󲿷������Ǽ̳���jQueryԭ�͵����ԣ�jQuery����ʵ����������һ������:
<img src='jQuery-Object.png'/>


�����������Ʋ⣬jQuery��ʵ�ֿ��������������ģ�
function jQuery(){
	this[0]="Some DOM Element";
	this[1]="Some DOM Element";
	this[2]="Some DOM Element";
	this.length=3;
	this.prevObject="Some Object";
	this.context="Some Object";
	this.selector="Some selector";
}
jQuery.prototype={
get:function(){},
each:function(){},
......
}
��Щ����ͨ��new�������;��ܴ�����ӵ���������Ե�jQuery����,����ʵ�������ǵ���jQuery����jQuery����ʱ��û��ʹ��new���������������ʵ�ֵ��أ�����jQuery��ʵ��:
var jQuery = function( selector, context ) {
		// The jQuery object is actually just the init constructor 'enhanced'
		return new jQuery.fn.init( selector, context, rootjQuery );
}
jQuery.fn=jQuery.prototype={
	jquery: core_version,
	init:function(selector,context){
		//some code
		return this;
	}
	//some code there
	//......
}
jQuery.fn.init.prototype=jQuery.fn;


