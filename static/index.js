// 예약
const handleReserve = (time, day, type, room) => {
    fetch('/reserve',{
        method : 'POST',
        headers: {
            'Content-Type': 'application/json',
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        body : JSON.stringify({
            time, day, type, room
        })
    }).then((res)=>{
        console.log(res);
        if(res.status===200){
            alert('예약이 완료되었습니다.');
            window.location.reload()
        }else if(res.status===401){
            return alert('로그인 정보가 없습니다. 로그인을 해 주세요.')
        }
    }).catch((e)=>{
        console.log(e);
        alert('에러가 일어났습니다.')
    })
}

// 예약 취소
const handleCancel = (time, day, type, room) => {
    if(!window.confirm('예약을 정말 취소하시겠습니까?')) return;

    fetch('/cancel',{
        method : 'POST',
        headers: {
            'Content-Type': 'application/json',
          },
        body : JSON.stringify({
            time, day, type, room
        })
    }).then((res)=>{
        if(res.status===200){
            alert('예약 취소가 완료되었습니다.');
            window.location.reload()
        }else if(res.status===401){
            return alert('로그인 정보가 없습니다. 로그인을 해 주세요.')
        }else if(res.status === 404){
            return alert('예약 정보가 없습니다.')
        }
    }).catch((e)=>{
        console.log(e);
        alert('에러가 일어났습니다.')
    })
}


// 시간 블럭 선택했을 때 함수
const pick = function (time, day, reservations, loginId) {
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

    //만약 timeTableDetail id element가 없다면 아예 박스를 새로 만들어야 하고, 아니라면 내부요소만 바꾸면 됨
    //상황을 나눈다.
    if(!document.getElementById('timeTableDetail')){
         //picked가 처음 눌린 상황 => element 전체 만들어야 함
         document.getElementById('detailWrapper').insertAdjacentHTML('beforeend',`<div id="timeTableDetail" class="flex flex-col w-48 h-64 border border-indigo-600"> 
         <div class="flex w-full justify-evenly h-1/2 items-center text-sm">
             <div id="detailLaundry325" class="flex justify-evenly w-full h-full flex-col items-center">
                 <div>
                     325
                 </div>
                 <div>
                     세탁기
                 </div>
                 <div id="detailLaundry325Bottom">
                     <button type="button" class=" ml-auto bg-blue-500 hover:bg-blue-700 text-white text-xs font-bold py-2 px-2.5 rounded ">예약하기</button>
                 </div>
             </div>
             <div id="detailLaundry326" class="flex justify-evenly w-full h-full flex-col items-center bg-amber-400 text-white	">
                 <div>
                     326
                 </div>
                 <div>
                     세탁기
                 </div>
                 <div id="detailLaundry326Bottom">
                     예약완료
                 </div>
             </div>
         </div>
         <div class="flex w-full justify-evenly h-1/2 items-center text-sm">
             <div id="detailDry325" class="flex justify-evenly w-full h-full flex-col items-center bg-amber-400 text-white	">
                 <div>
                     325
                 </div>
                 <div>
                     건조기
                 </div>
                 <div id="detailDry325Bottom">
                     예약완료
                 </div>
             </div>
             <div id="detailDry326" class="flex justify-evenly w-full h-full flex-col items-center ">
                 <div>
                     326
                 </div>
                 <div>
                     건조기
                 </div>
                 <div id="detailDry326Bottom">
                     <button type="button" class=" ml-auto bg-blue-500 hover:bg-blue-700 text-white text-xs font-bold py-2 px-2.5 rounded ">예약하기</button>
                 </div>
             </div>
         </div>
     </div>`)
        
    }

    //pickedReserve 결과에 따라 선택박스 채워야 함
    //만약 laundry면 위쪽 박스에서 room 호수에 따라 첫번째/두번째 엘리먼트 선택
    //만약 dry면 아래쪽 박스에서 room 호수에 따라 첫번째/두번째 엘리먼트 선택
    //pickedReserve에 없는 애는 예약하기 버튼 살려야 함
    for(let type of ['Laundry','Dry']){
        for(let room of ['325','326']){
            if(pickedReserve.some(({ type:etype, room:eroom, user})=>{return etype.toLowerCase() === type.toLowerCase() && eroom === room})){
                //예약있음. 예약 불가능상태

                if(!loginId){
                    document.getElementById(`detail${type}${room}`).className = 'flex justify-evenly w-full h-full flex-col items-center bg-amber-400 text-white'
                    document.getElementById(`detail${type}${room}Bottom`).innerHTML = '예약완료';
                }else{
                    //로그인 있으면 내 예약인지 아닌지 한번 확인하기
                    const {user} = pickedReserve.find(({ type:etype, room:eroom})=>{return etype.toLowerCase() === type.toLowerCase() && eroom === room});
                    if(typeof user === 'string' ? user : user.toString() === loginId.toString()){
                        document.getElementById(`detail${type}${room}`).className = 'flex justify-evenly w-full h-full flex-col items-center bg-green-500 text-white'
                        document.getElementById(`detail${type}${room}Bottom`).innerHTML = `<button type="button" class="ml-auto bg-amber-500 hover:bg-amber-700 text-white text-xs font-bold py-2 px-2.5 rounded" onclick="handleCancel('${time}','${day}','${type.toLowerCase()}', '${room}')">예약 취소</button>`;
                    }else{
                        document.getElementById(`detail${type}${room}`).className = 'flex justify-evenly w-full h-full flex-col items-center bg-amber-400 text-white'
                        document.getElementById(`detail${type}${room}Bottom`).innerHTML = '예약완료';
                    }
                }
                
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
  }).then(()=>location=location)
}

