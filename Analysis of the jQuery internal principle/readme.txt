这段时间在学习研究jQuery源码，受益于jQuery日益发展强大，研究jQuery的大牛越来越多，学习的资料也比前两年好找了，有很多非常不错的资源，如高云的<a href="http://www.cnblogs.com/nuysoft/archive/2011/11/14/2248023.html" target="_blank">jQuery1.6.1源码分析系列</a>。这些教程非常细致的分析了jQuery内部原理和实现方式，对学习和理解jQuery有非常大的帮助。但是个人认为很多教程对jQuery的整体结果把握不足，本人试图从整体来阐述一下jQuery的内部实现。<!--more-->

大家知道，调用jQuery有两种方式，一种是高级的实现，通过传递一个参数实现DOM选择，如通过$("h1")选择所有的h1元素，第二种是较为低级的实现，如果通过$.ajax实现ajax的操作。那么，这两种方式到底有何不同？用typeof函数检测$('h1')和$.ajax,类型分别为object和function，稍微学过jQuery的都知道或者听过过，前者返回的是一个jQuery对象，那么jQuery对象是什么，它和jQuery是什么关系呢？我们先来通过for(var i in $('')) document.write(i+" :::"+$("")[i]+"");打印一下jQuery对象的属性和对应的值,可以看到它有100多个属性，通过console输入$("*")可以看到大部分属性是继承自jQuery原型的属性，jQuery对象实际上是这样一个对象:

![image](https://github.com/hitoy/post/blob/master/Analysis%20of%20the%20jQuery%20internal%20principle/jQuery-Object.png)

所以我们来推测，jQuery的实现可能是类似这样的：
<pre language='javascript'>
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
</pre>
这些代码通过new操作符就就能创建出拥有上述属性的jQuery对象,但是实际上我们调用jQuery创建jQuery对象时并没有使用new操作符，这是如何实现的呢？来看jQuery的实现:
<pre language='javascript'>
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
</pre>
这里有几点做得非常巧妙的地方,第一点是通过jQuery原型属性的init方法来创建对象来达到不用new创建对象的目的，第二点是对init方法内this指向的处理。我们知道，通过调用init返回一个jQuery的实例，那么这个实例就必须要继承jQuery.prototype的属性，那么init里面这个this, 就继承jQuery.prototype的属性。但是init里面的this，受制于作用域的限制，并不能访问jQuery.prototype其它的属性，jQuery通过一句'jQuery.fn.init.prototype=jQuery.fn'把它的原型指向jQuery.fn,这样以来，init产生的jQuery对象就拥有了jQuery.fn的属性。

到这里，一个jQuery的基本原型就浮出水面了。这里有两个对象，一个是jQuery这个构造函数，另外一个是这个构造函数产生的对象(我们称之为jQuery对象，它和普通对象没有什么区别), 如下关系图:

![image](http://www.hitoy.org/wp-content/uploads/jQuery-construct.png)
可以看到jQuery构造函数和jQuery.prototype均有各自的属性和方法，两者的调用方法各不一样,这两个对象都有一个extend方法，都是用来扩展自身的属性和方法，在jQuery内部，extend的实现实际是靠一样的代码, 将在后面的源码分析中做以详细的分析。
