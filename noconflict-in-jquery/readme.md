jQuery中noconflict的实现原理
============================

jQuery中，noconflict是用来防止变量冲突，用来释放变量控制权的一个重要方法。我们知道，jQuery中对外提供有两个全局变量，$和jQuery，虽然jQuery只产生了两个全局变量，极少情况下才会出现冲突，但是如果网页中如果包涵较多的类库,有自定义$或jQuery全局变量的存在时，就会存在冲突的情况。

jQuery提供的noconflict函数很好的解决了变量冲突问题，无论是$或者jQuery冲突都可以解决，接下来我们就来分析一下jQuery的冲突处理。

先来看一下jQuery源码中noconflict的实现:
<pre language="javascript">
(function(window,undefined){
var 
// Map over jQuery in case of overwrite
_jQuery = window.jQuery,

// Map over the $ in case of overwrite
_$ = window.$,

jQuery.extend({
noConflict: function( deep ){
	if ( window.$ === jQuery ) {
		window.$ = _$;
	}
	if ( deep && window.jQuery === jQuery ) {
		window.jQuery = _jQuery;
	}
	return jQuery;
}
})
}(window)
</pre>
在这里jQuery.extend是jQuery扩展静态属性的方法，这里可以看成直接在jQuery上附加noConflict方法。在匿名函数的内部，分别定义内部变量_jQuery和_$用来存储window.jQuery和window.$, 这么做的用作在于用内部变量保存jQuery运行之前这两个全局变量的状态, 以便在后面的防冲突操作中还原这两个变量。noConflict可处理$和jQuery这两个变量冲突的情况，默认处理$,传入一个true参数，则处理jQuery冲突的情况。

window.$ === jQuery用来判断全局变量是否等于jQuery，如果等于，则重新还原全局变量$为jQuery运行之前的变量(存储在内部变量  中)；deep && window.jQuery === jQuery 当开启深度冲突处理并且全局变量jQuery等于内部jQuery，则把全局jQuery还原成之前的状况。判断window.$ === jQuery和window.jQuery=jQuery的意义在于保护已经定义的变量不被重写，如下面的代码：

<pre language=''javascript>
//引入jQuery库
var $="String";
var jq=jQuery.noconflict();
var jQuery="This is a line";
var j=jq.noconflict(true);
console.log($);//这里如果没有window.$===jQuery这句判断，那么$将会等于undefined而不是"String"。
console.log(jQuery); //同上，如果没有判断window.jQuery===jQuery，重新定义的jQuery就会被undefined覆盖。
</pre>

noConflict返回的是jQuery这个构造函数, 用最新的变量存储, 像使用$一样尽情使用它吧!
