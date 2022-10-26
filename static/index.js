const handleReserve = (time, day, type, room) => {
    fetch('/reserve',{
        method : 'POST',
        body : {
            time, day, type, room
        }
    }).then((res)=>{
        console.log(res)
    }).catch((e)=>{
        console.log(e);
    })
}


// 시간 블럭 선택했을 때 함수
const pick = function (time, day, reservations) {
    //picked를 갖고 있는 엘리먼트의 전체 클래스 반환
    const beforeClass = document.getElementsByClassName('picked');

    //기존에 picked 있던 엘리먼트에서 pick 제거
    if(beforeClass.length>0){
        const slicedClass = beforeClass.item(0).className.slice(0,-6);
        beforeClass.item(0).className = slicedClass
    }

    //새로 pick한 엘리먼트에 border 효과 적용
    document.getElementById(`${day}-${time}`).className+=" picked";

    //들어온 reservations에서 day, time에 해당하는 예약 있는지 확인
    //day는 reservations를 가져올 때 해당하는 걸 주므로 확인 안해도 됨
    const pickedReserve = reservations.filter(({time:obTime})=> time === obTime );

    //pickedReserve 결과에 따라 선택박스 채워야 함
    //만약 laundry면 위쪽 박스에서 room 호수에 따라 첫번째/두번째 엘리먼트 선택
    //만약 dry면 아래쪽 박스에서 room 호수에 따라 첫번째/두번째 엘리먼트 선택
    //pickedReserve에 없는 애는 예약하기 버튼 살려야 함
    for(let type of ['Laundry','Dry']){
        for(let room of ['325','326']){
            if(pickedReserve.some(({type:etype,room:eroom})=>{return etype.toLowerCase() === type.toLowerCase() && eroom === room})){
                //예약있음. 예약 불가능상태
                document.getElementById(`detail${type}${room}`).className = 'flex justify-evenly w-full h-full flex-col items-center bg-amber-400 text-white'
                document.getElementById(`detail${type}${room}Bottom`).innerHTML = '예약완료';
            }else{
                //예약없음. 예약 가능상태
                document.getElementById(`detail${type}${room}`).className = 'flex justify-evenly w-full h-full flex-col items-center'
                document.getElementById(`detail${type}${room}Bottom`).innerHTML = `<button type="button" class="ml-auto bg-blue-500 hover:bg-blue-700 text-white text-xs font-bold py-2 px-2.5 rounded" onclick="handleReserve('${time}','${day}','${type.toLowerCase()}', '${room}')">예약하기</button>`;
            }
        }
    }
}


const logOut = function() {
    fetch('/logout',
  {
    method: 'GET',
  }).then(location=location)
  .then(location=location)
  .then(location=location)
}

