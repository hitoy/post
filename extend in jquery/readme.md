jQuery中extend的实现原理
========================

extend()是jQuery中一个重要的函数，作用是实现对对象的扩展, 它经常用于jQuery插件的开发，jQuery内部也使用它来扩展属性方法，如上篇文章中讲到的noConflict方法，就是用extend方法来扩展的。

![extend function in jQuery](extend-in-jquery.jpg)

在jQuery的API手册中，我们看到，extend实际上是挂载在jQuery和jQuery.fn上的两个不同方法，尽管在jQuery内部jQuery.extend()和jQuery.fn.extend()是用相同的代码实现的，但是它们的功能却不太一样。来看一下<a href="http://api.jquery.com/?s=extend">官方API对extend的解释</a>:
jQuery.extend(): Merge the contents of two or more objects together into the first object.(把两个或者更多的对象合并到第一个当中)
jQuery.fn.extend():Merge the contents of an object onto the jQuery prototype to provide new jQuery instance methods.(把对象挂载到jQuery的prototype属性，来扩展一个新的jQuery实例方法)

我们知道，jQuery有静态方法和实例方法之分, 那么jQuery.extend()和jQuery.fn.extend()的第一个区别就是一个用来扩展静态方法，一个用来扩展实例方法。用法如下:
<pre language="javascript">
jQuery.extend({
	sayhello:function(){
			console.log("Hello,This is jQuery Library");
		}
})
$.sayhello();	//Hello, This is jQuery Library

jQuery.fn.extend({
	check: function() {
		return this.each(function() {
		this.checked = true;
		});
	},
	uncheck: function() {
		return this.each(function() {
			this.checked = false;
		});
  }
})
$( "input[type='checkbox']" ).check(); //所有的checkbox都会被选择
</pre>
注意两种调用插件的方式，一种是直接用$调用，另外一种是用$()调用，另外jQuery.extend()接收多个对象作为参数，如果只有一个参数，则把这个对象的属性方法附加到jQuery上，如果含有多个参数，则把后面的对象的属性和方法附加到第一个对象上。jQuery extend的实现源码:
<pre language="javascript">
jQuery.extend = jQuery.fn.extend = function() {
	var options, name, src, copy, copyIsArray, clone,
		target = arguments[0] || {},
		i = 1,
		length = arguments.length,
		deep = false;

	// Handle a deep copy situation
	if ( typeof target === "boolean" ) {
		deep = target;
		target = arguments[1] || {};
		// skip the boolean and the target
		i = 2;
	}

	// Handle case when target is a string or something (possible in deep copy)
	if ( typeof target !== "object" && !jQuery.isFunction(target) ) {
		target = {};
	}

	// extend jQuery itself if only one argument is passed
	if ( length === i ) {
		target = this;
		--i;
	}

	for ( ; i < length; i++ ) {
		// Only deal with non-null/undefined values
		if ( (options = arguments[ i ]) != null ) {
			// Extend the base object
			for ( name in options ) {
				src = target[ name ];
				copy = options[ name ];

				// Prevent never-ending loop
				if ( target === copy ) {
					continue;
				}

				// Recurse if we're merging plain objects or arrays
				if ( deep && copy && ( jQuery.isPlainObject(copy) || (copyIsArray = jQuery.isArray(copy)) ) ) {
					if ( copyIsArray ) {
						copyIsArray = false;
						clone = src && jQuery.isArray(src) ? src : [];

					} else {
						clone = src && jQuery.isPlainObject(src) ? src : {};
					}

					// Never move original objects, clone them
					target[ name ] = jQuery.extend( deep, clone, copy );

				// Don't bring in undefined values
				} else if ( copy !== undefined ) {
					target[ name ] = copy;
				}
			}
		}
	}

	// Return the modified object
	return target;
};
</pre>
很大一堆代码，乍看起来难以理解，其实代码的大部分都是用来实现jQuery.extend()中有多个参数时的对象合并，深度拷贝问题，如果去掉这些功能，让extend只有扩展静态和实例方法的功能，那么代码如下:
<pre language="javascript">
jQuery.extend = jQuery.fn.extend = function(obj){
	//obj是传递过来扩展到this上的对象
	var target=this;
	for (var name in obj){
			//name为对象属性
			//copy为属性值
			copy=obj[name];
			//防止循环调用
			if(target === copy) continue;
			//防止附加未定义值
			if(typeof copy === 'undefined') continue;
			//赋值
			target[name]=copy;
	}
	return target;
}
</pre>
下面再来对extend方法进行注释解释:
<pre language="javascript">
jQuery.extend = jQuery.fn.extend = function() {
	// 定义默认参数和变量
	// 对象分为扩展对象和被扩展的对象 
	//options 代表扩展的对象中的方法
	//name 代表扩展对象的方法名
	//i		为扩展对象参数起始值
	//deep 默认为浅复制
	var options, name, src, copy, copyIsArray, clone,
		target = arguments[0] || {},
		i = 1,
		length = arguments.length,
		deep = false;

	//当第一个参数为布尔类型是，次参数定义是否为深拷贝
	//对接下来的参数进行处理
	if ( typeof target === "boolean" ) {
		deep = target;
		target = arguments[1] || {};
		// 当定义是否深拷贝时，参数往后移动一位
		i = 2;
	}

	// 如果要扩展的不是对象或者函数，则定义要扩展的对象为空
	if ( typeof target !== "object" && !jQuery.isFunction(target) ) {
		target = {};
	}

	// 当只含有一个参数时，被扩展的对象是jQuery或jQuery.fn
	if ( length === i ) {
		target = this;
		--i;
	}

	//对从i开始的多个参数进行遍历
	for ( ; i < length; i++ ) {
		// 只处理有定义的值
		if ( (options = arguments[ i ]) != null ) {
			// 展开扩展对象
			for ( name in options ) {
				src = target[ name ];
				copy = options[ name ];

				// 防止循环引用
				if ( target === copy ) {
					continue;
				}

				// 递归处理深拷贝
				if ( deep && copy && ( jQuery.isPlainObject(copy) || (copyIsArray = jQuery.isArray(copy)) ) ) {
					if ( copyIsArray ) {
						copyIsArray = false;
						clone = src && jQuery.isArray(src) ? src : [];

					} else {
						clone = src && jQuery.isPlainObject(src) ? src : {};
					}

					target[ name ] = jQuery.extend( deep, clone, copy );

				// 不处理未定义值
				} else if ( copy !== undefined ) {
					//给target增加属性或方法
					target[ name ] = copy;
				}
			}
		}
	}

	//返回
	return target;
};
</pre>

弄懂了jQuery扩展的原理，相信以后再也不用为编写jQuery插件而烦恼了。
