$(function(){
	
	// 랜덤 난수를 뽑기 위한 함수
	var getRandomInt = function (min, max) {
		min = Math.ceil(min);
		max = Math.floor(max);
		return Math.floor(Math.random() * (max - min)) + min; //최댓값은 제외, 최솟값은 포함
	}
	var p = {
		// 버튼누르고 난 다음 바로 호출되는 GUI를 위한 함수 
		startCallback : function() {
			$('.start').attr('disabled', 'true');
			$('.stop').removeAttr('disabled');
		},
		slowDownCallback : function() {
			$('.stop').attr('disabled', 'true');
		},
		stopCallback : function($stopElm) {
			$('.start').removeAttr('disabled');
			$('.stop').attr('disabled', 'true');
		}

	}
	
	var rouletter = $('div.roulette');
	rouletter.roulette(p);
	// 시작하자마자 자동으로 돌아가도록
	rouletter.roulette('start');
	

	// 첫실행시 바로 꺼지는 에러 방지	
	let flag = true 
	// 멈춤 버튼을 누르면 난수 생성 -> 이미지 이름값으로 넘겨줌
	$('.stop').click(function(){
		// 무작위 범위 == 사진 갯수
		var RandomInt = getRandomInt(1, 10)
		console.log(RandomInt)
		var updateParamater = function(){
      p['stopImageNumber'] = RandomInt
      console.log(typeof(RandomInt))
			rouletter.roulette('option', p);	
		} 
		updateParamater();
		// 변경된 값으로 사용하기 위해 flag를 false로 만듬
		flag = false 
		rouletter.roulette('stop');	
	});
	$('.stop').attr('disabled', 'true');
	$('.start').click(function(){
		rouletter.roulette('start');	
	});
	
	// 처음 실행을 위한 값 
	if (flag === true) {
	var updateParamater = function(){
		p['stopImageNumber'] = 3
		// 시작할때 random으로 돌리고 stop버튼 활성화
		$('.stop').removeAttr('disabled');
		rouletter.roulette('option', p);	
	}
	updateParamater();
}


});

