

// 시간 블럭 선택했을 때 함수
const pick = function (time, day) {
    //picked를 갖고 있는 엘리먼트의 전체 클래스 반환
    const beforeClass = document.getElementsByClassName('picked');

    if(beforeClass.length>0){
        const slicedClass = beforeClass.item(0).className.slice(0,-6);
        beforeClass.item(0).className = slicedClass
    }
    document.getElementById(`${day}-${time}`).className+=" picked";
}