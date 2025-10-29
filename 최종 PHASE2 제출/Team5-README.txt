README.txt

						[ SQL 실행 순서 ]
1. CREATE_TABLE_DDL.sql
2. INSERT_RECORD_ALL.sql
						[ 테이블 전체 삭제를 원한다면 ]
1. DELETE_TABLE_ALL.sql


						[ 간단 기획 설명 ]
개인 빚을 갚기 위해 고향으로 내려와 전당포를 이어 운영하기로 하였다
물건의 흠을 찾거나, 진위 여부, 숨겨진 가치 등급을 밝혀내 
구매 가격을 낮추거나 감정 가격을 높여서
싸게 사서 비싸게 파는 게 목적이다.
이 과정에서 대출을 받거나, 경매에 아이템을 내놓거나 기습 이벤트(뉴스)가 발생할 수 있다.

이자를 못 내게 되면, 게임 오버
개인 빚을 모두 갚으면 게임 클리어

게임을 클리어하면, 세계 기록에 기록을 남길 수 있다.


						[ 세부 기획 목차 ]
[거래 전 동작]
	- 뉴스 이벤트 발생
	- 손님 접수
		- 판매
		- 거래
[거래 중 동작]
	- 아이템 힌트 열람
	- 고객 뒷조사 (고객 힌트 열람)
	- 흠 찾기
	- 진위 판정
	- 감정
	- 거래하기
	- 거래 안 하기
[거래 후 동작]
	- 전시장 해금
	- 복원
	- 경매
	- 대출
	- 대출 상환하기
	- 다음 날 넘어가기
[게임 외부]
	- 게임 오버
	- 게임 클리어
	- 로그인/회원가입
	- 세계 기록 확인



						[ 세부 기획 ]
[거래 전 동작]
	- 뉴스 이벤트 발생
		: 플레이어의 DAY_COUNT가 1일차를 제외한 7의 배수일차일 때마다 이벤트가 발생합니다.
			이벤트가 발생하면, 이전 이벤트가 있다면, 이전 이벤트는 삭제합니다.
			뉴스 이벤트를 임의의 카탈로그_ID 랜덤하게 1~3개의 이벤트를 생성시킨 뒤, DB에 넣습니다 (이벤트는 중복이 가능합니다.)
		이벤트 한번에 생성되는 개수
		0: 30 %
		1: 40 %
		2: 20 %
		3: 10 %


			뉴스이벤트는 최초 제시가, 거래가, 감정가, 최종 판매가 중 하나에 영향을 끼치며, 영향의 정도는 임의의 -50~50(%)입니다.
	-손님 접수(매일 3명)
		- 판매
			: 전시 중인 아이템이 있음
				→ 손님의 선호 카테고리와 아이템의 카테고리가 동일함 → 구매를 시도함
					→ 판매하지 않는다면, 거래가 시작됨
					→ 판매한다면, 감정가의 20% 할인 된 금액으로 구매해감. 
		- 거래 시작

[거래 중 동작]

  [ 필드 ]
	- 최초 제시가
		: 고객이 최초로 제시하는 가격 
	- 구매가
		: 최초 제시가와 동일합니다. [거래 중] 흠 찾기, 진위 판정 등을 통해 하락시킬 수 있습니다.
	- 감정가
		: 최초 제시가와 동일합니다. [거래 중] 흠 찾기, 진위 판정, 감정 등을 통해 변화되며, [거래 후]에는 복원을 통해 변화시킬 수 있습니다.
	- 최종 판매가
		: 	[ 거래 중 ] 미표시.
			[ 거래 전 ] 손님에게 판매하는 경우, 현재 감정가의 20%를 할인 한 금액으로 설정됩 후 판매 됩니다.
			[ 거래 후 ] 경매로 판매하는 경우, 현재 감정가의 랜덤하게 1.2~1.5배 증가된 금액으로 설정된 후 판매 됩니다.

  [ 동작 ]
	[서버] DB에 아이템, 거래 생성

	[고객 필드]
		사기정도 0.0~1.0
		잘수집정도 0.0~1.0
		부주의함 0.0~1.0
			흠이 있을 삘(랜덤 변수) 0.0~1.0

	[아이템 필드]
		흠 개수 0~14개
			:  ( 0+ 10 * 부주의함 ) + (0 + 4 * 흠이 있을 삘) 개

		진위 여부 T/F
			: 	가품 확률값: ( 10 + 90 * 사기 정도 ) (%)
				진품 확률값: (100 - 가품 확률)(%)

		등급 0~3 /일반~레전더리
			:	레전더리 확률값: 	15 + (65 * 잘수집정도 )
				   유니크 확률값: 	20 + ( (65 * (1 - 잘수집정도) ) /3 ) (%)
				      레어 확률값: 	30 + ( (65 * (1 - 잘수집정도) ) /3 ) (%)
				      일반 확률값: 	35 + ( (65 * (1 - 잘수집정도) ) /3 ) (%)
			
		최초 제시가
			: 	기준가 = 아이템 카탈로그- 베이스가격
			최초 제시가 = 기준가	×[(1−0.02×흠 개수)
							×(1−0.3×가품 확률)
							×((1+0.3×등급)/3)
							×(1+0.25×사기 정도)
							×(1+0.2×(수집력−0.5))]

	- 아이템 힌트 열람
		아이템 이미지 아래에 아이템 힌트 열람 [ 10 G ] 버튼 6개
			- 흠이 있을 것 같은 삘 0.0~1.0
			- 레전더리 확률값
			- 유니크 확률값
			- 레어 확률값
			- 진품 확률값
			- 최소 몇개 이상 ( (0+10 * 부주의함) *(0.8) )
		힌트의 정렬 순서는 랜덤

	- 고객 뒷조사 (고객 힌트 열람)
		고객 이미지 아래에 아이템 힌트 열람 [ 20 G ] 버튼 3개
			- 사기정도 0.0~1.0
			- 잘수집정도 0.0~1.0
			- 부주의함 0.0~1.0
		힌트의 정렬 순서는 사기정도, 잘수집정도, 부주의함
		그 고객으로부터 한번 열람한 정보는 다음에 방문 했을 때에도 여전히 확인 가능함(PLAYER_CUSTOMER_HIDDEN_DISCOVERED)
		

	- 흠 찾기 (여러 번 시행 가능)
		: 흠을 찾았다면, 구매가와 감정가가 흠의 개수 x 5% 만큼 하락합니다. (최대 70% 하락, 최대 흠 개수 14개)
			- 고급 흠 찾기	[ 100 G ]
				: 만약 흠이 그만큼 있다면, 최대 7개의 흠을 찾아냅니다.
			- 중급 흠 찾기	[  60 G ]
				: 만약 흠이 그만큼 있다면, 최대 4개의 흠을 찾아냅니다.
			- 하급 흠 찾기	[  20 G ]
				: 만약 흠이 그만큼 있다면, 최대 1개의 흠을 찾아냅니다.
	- 진위 판정	[  200 G ]
		: 진품/가품 상태를 확정시킵니다.
			진품이었다면, 가격에 변동이 없습니다.
			가품이었다면, 구매가가 50% 하락합니다. 감정가는 20% 하락합니다. (최종 판매 시, 30% 이득)
			- 만약 미확정 상태에서 복원을 시도하면,
				진품이었다면, 가격에 변동이 없습니다.
				가품이었다면, 감정가 30% 하락합니다.
	- 감정 (여러 번 시행 가능)
		-숨겨진 등급을 확률에 따라 확정시킵니다.
			- 레전더리 감정	[  50 G ]
				: 아이템의 숨겨진 등급에 따라 최대 레전더리 등급까지 확정시킬 수 있습니다.
			- 유니크 감정	[  30 G ]
				: 아이템의 숨겨진 등급에 따라 최대 유니크 등급까지 확정시킬 수 있습니다.
			- 레어 감정		[  20 G ]
				: 아이템의 숨겨진 등급에 따라 최대 레어 등급까지 확정시킬 수 있습니다.
		- 등급이 확정되면, 감정가가 아래 표에 따라 증가합니다.
			레전더리	: 감정가가 최초 제시가의 1.7배로 증가합니다.
			유니크	: 감정가가 최초 제시가의 1.5배로 증가합니다.
			레어		: 감정가가 최초 제시가의 1.2배로 증가합니다.
		- 등급 확정 확률표
			아이템이 레전더리 등급이라면,
				일반		: 10%
				레어		: 20%
				유니크	: 30%
				레전더리	: 40%
			아이템이 유니크 등급이라면,
				일반		: 20%
				레어		: 30%
				유니크	: 50%
			아이템이 레어 등급이라면,
				일반		: 30%
				레어		: 70%
		
	- 거래 하기
		[DB] 아이템 - 상태 : 전시 중으로 변경
		[DB] 최초 제시가, 구매가는 이제 고정.
		
	- 거래 안 하기
		[서버] DB에 아이템, 거래 제거

[거래 후 동작]

  [ 필드 ]
	- 최초 제시가 ▶ 최초 제시가 * (이벤트 수치(적용 중인 뉴스)* ~최대 3개)

	- 구매가 ▶ 최초 제시가 * (1 - 밝혀낸 흠 개수 * 5%) * 감정 등급(1.0~1.7) * (1 - 거래 중 진품 여부(FALSE =1) * 50%)   * (이벤트 수치(적용 중인 뉴스)* ~최대 3개)

	- 감정가 ▶ 최초 제시가 * (1 - 밝혀낸 흠 개수 * 5% + 수리한 흠 개수 * 5%) * 감정 등급(1.0~1.7) 
					* (1 - 거래 중 진품 여부(FALSE =1) * 20%) * (1 - 복원 중 진품 여부(FALSE =1) * 30%)  * (이벤트 수치(적용 중인 뉴스)* ~최대 3개)

	- 최종 판매가 ▶ 감정가 * (1 - 고객 판매 여부(TRUE=1) * 20%) * (경매 판매 여부(TRUE=1) *(1.3~1.7))
						* (1- 진품 여부 미확정 상태(TRUE =1) * 40% ) * (이벤트 수치(적용 중인 뉴스)* ~최대 3개)
		: 	[ 거래 중 ] 미표시.
			[ 거래 전 ] 손님에게 판매하는 경우, 현재 감정가의 20%를 할인 한 금액으로 설정됩 후 판매 됩니다.
			[ 거래 후 ] 경매로 판매하는 경우, 현재 감정가의 랜덤하게 1.2~1.5배 증가된 금액으로 설정된 후 판매 됩니다.
	- [전시장]
		- 아이템 추가 시,
			[DB] 전시 아이템 테이블(GAME_SESSION_ITEM_DISPLAY)에 비어있는 가장 빠른 DISPLAY_POS 번호에 INSERT
				EX. [전시 위치] 카테고리 번호 : 
						[0] 1
						[1]      << INSERT
						[2] 3
						[3] 2
						[4] 
						[5] 
		- 아이템 판매 시,
			[DB] 전시 아이템 테이블(GAME_SESSION_ITEM_DISPLAY)에 카테고리가 일치하는 아이템 중 임의의 DISPLAY_POS 아이템 판매 및 DELETE
            [DB] DEAL_RECORD 테이블의 BOUGHT_DATE 속성에 GAME_SESSION 테이블의 DAY_COUNT 값을 대입
				EX. [전시 위치] 카테고리 번호 : 
						[0] 1
						[1] 2 <<
						[2] 3
						[3] 2 <<
						[4] 4
						[5] 2 <<
					카테고리 번호가 2인 전시 위치 1,3,5 중 랜덤 위치 3 선택.
					

  [ 동작 ]
	- 전시장 해금
		: 최초 2개까지 전시 가능.
		[ 1000 G ] 4개로 확장
		[ 2000 G ] 8개로 확장
		
	- 복원
		: 전시 중인 아이템을 복원 전문가에게 맡긴다.
			1. 흠 수리
				: 흠 당 10 골드를 소모하여 흠을 수리합니다.
				: 수리한 흠 당 감정가가 5% 증가합니다.
			2. 진위 판정(흠 수리 시 자동 판정 됩니다.)
				: 미확정 상태라면,
					진품이라면, 감정가에 변동이 없습니다.
					가품이라면, 감정가가 30% 하락합니다.
				: 확정 상태라면, 감정가에 변동이 없습니다.
		미 수리하여, 미확정 상태에서 판매 시, 최종 판매가는 40% 하락합니다.
		복원에는 1일이 소모 됩니다. 
		복원 중에는 아이템이 잠금 상태가 되어, 해당 전시장 위치를 사용할 수 없습니다.

	- 경매
		: 경매는 3의 배수 일차마다 열린다.
		경매 출품 중에는 아이템이 잠금 상태가 되어, 해당 전시장 위치를 사용할 수 없다.
		경매에는 1일이 걸린다.
		경매가 완료 되면, 아이템은 전시장에서 사라진다. 정산금을 알려준다.
		경매가 완료 된 후, 1일 후 정산금이 들어온다.

		경매의 경우, 거래 - 구매 고객에 고객키로 0번(경매인)이 들어간다.
        [DB] DEAL_RECORD 테이블의 BOUGHT_DATE 속성에 GAME_SESSION 테이블의 DAY_COUNT 값을 대입


	- 대출
		: 매일 [거래 후]일 때, 대출을 받을 수 있다
			- [ 2,000G ] 
			- [ 1,000G ] 
			- [   500G ] 
			- [   300G ]

	- 대출 상환하기
		[거래 후]에는 대출 빚을 상환할 수 있다.		
		- 개인 빚( 기본 500,000 골드 )
			: 원하는 금액만큼 입력 후 상환 버튼을 누른다
		- 대출 빚
			- 각 대출이 표시 된다.
			- 대출 객체를 선택하면, 
			- 대출 빚 상환 버튼 아래에  개인 빚, 전당포 빚을 띄운다. << GAME_SESSION 테이블의 PERSONAL_DEBT, PAWNSHOP_DEBT 이 쓰이는 곳
			: 원하는 금액만큼 입력 후 상환 버튼을 누른다.

	- 다음 날 넘어가기
      - 정산
         + 오늘 시작 잔금 << 속성 추가해야 함
         - 오늘 구매 금액 << 속성 추가해야 함
         + 오늘 판매 금액 << 기존 Sold_date 속성 이용
         - 대출 빚 이자 (총 대출 빚의 5%) << 기존 Pawnshop debt 속성 이용
         ------------------------------
         오늘 최종 잔금 표시

      - 7의 배수 일차마다 정산
         + 오늘 시작 잔금
         - 오늘 구매 금액
         + 오늘 판매 금액
         - 개인 빚 이자 (개인 빚의 0.05%) ← (유저 -개인 빚) * 0.005 << 기존 Personal debt 속성 이용
         - 대출 빚 이자 (총 대출 빚의 5%) ← SUM(대출 - 남은 대출 금액) * 0.05 << 기존 Pawnshop debt 속성 이용
         ------------------------------
         오늘 최종 잔금 표시

		개인 빚은 이자율이 적은 대신 게임을 클리어하는데 필요
		전당포 빚은 이자율이 높고 매일 내야 함.
			>> 무조건 전당포 빚을 먼저 갚도록 강요

		만약, 이자를 내지 못한다면, 게임 오버

[게임 외부]
	- 게임 오버
		: 개인 빚에 대한 이자를 못 내게 되면, 게임이 오버 됩니다.
            DB 속 GAME_SESSION 테이블의 CLEAR_END_DAY_COUNT 속성에 게임 오버했을 당시의 게임 일수의 음수 값을 넣습니다.
			DB 속 거래, 아이템은 유지됩니다.
			DB 속 아이템의 활성화 여부가 비활성화가 됩니다.
			DB 속 거래의 활성화 여부가 비활성화가 됩니다.
	- 게임 클리어
		- 대출(전당포) 빚과 개인 빚을 모두 갚으면, 게임을 클리어하게 됩니다.
            DB 속 GAME_SESSION의 CLEAR_DAY_COUNT는 클리어 한 시점의 DAY_COUNT, CLEAR_DATE는 현재 날짜를 입력합니다.
			DB 속 거래, 아이템은 유지됩니다.
			DB 속 아이템의 활성화 여부가 비활성화가 됩니다.
			DB 속 거래의 활성화 여부가 비활성화가 됩니다.
	- 로그인/회원가입
		- 회원가입
			회원 가입 버튼을 누른다
				아이디와 비밀번호를 입력한다
				아이디 중복 시 다시 입력하게 한다
		- 로그인
			아이디와 비밀번호를 입력한다



					[ DB 테이블 목차 ]
 1. 유저(PLAYER)
 2. 게임 세션(GAME_SESSION)   
 3. 고객 카탈로그(CUSTOMER_CATALOG)
 4. 아이템 카테고리(ITEM_CATEGORY) : 20개 레코드(상세 설명은 아래 엔티티)
 5. 아이템 카탈로그(ITEM_CATALOG)
 6. 아이템(EXISTING_ITEM)
 7. 거래(DEAL_RECORD)
 8. 플레이어-고객 비밀 발견(CUSTOMER_HIDDEN_DISCOVERED_IN_GAME_SESSION) <관계>
 9. 플레이어-아이템 전시(GAME_SESSION_ITEM_DISPLAY) <관계>
10. 뉴스(EXISTING_NEWS)
11. 뉴스 카탈로그(NEWS_CATALOG)


					[ DB 엔티티 ]




					[sql 쿼리문 설명]

쿼리문 자체에서 콘솔 입력을 받을 방법은 없는데, JDBC 라이브러리를 쓸 때는 쿼리를 문자열 형태로 넘기므로, 자바 String을 조작할 수 있음.
JDBC를 활용할 때는, player = 1에서 1을 조회하기를 원하는 Player의 Primary Key로 바꾸어 사용할 것임.


-- 플레이어 정보
SELECT * FROM GAME_SESSION WHERE PLAYER_KEY = 1 ORDER BY GAME_SESSION_KEY DESC FETCH FIRST ROW ONLY;
임의의 플레이어 (여기서는 1)인 행만 선택하고, 게임 세션 키를 내림차순 정렬, 가장 위에 있는 튜플을 가져온다. 



-- 진열대 정보 (Type 8)
SELECT D.DISPLAY_POS, I.*, IC.*
FROM GAME_SESSION_ITEM_DISPLAY D, EXISTING_ITEM I, ITEM_CATALOG IC
WHERE
    D.GAME_SESSION_KEY = (
        SELECT GAME_SESSION_KEY FROM GAME_SESSION
        WHERE PLAYER_KEY = 1
        ORDER BY GAME_SESSION_KEY DESC
        FETCH FIRST ROW ONLY
    )
    AND D.ITEM_KEY = I.ITEM_KEY
    AND I.ITEM_CATALOG_KEY = IC.ITEM_CATALOG_KEY
ORDER BY D.DISPLAY_POS;

임의의 플레이어 (여기서는 1)의 가장 최근 게임 세션에서 진열된 아이템들과 
그 아이템의 카탈로그 정보를 진열 순서대로 조회하는 쿼리.


-- 당일자 Event
SELECT * FROM EXISTING_NEWS N, NEWS_CATALOG NC
WHERE
    N.GAME_SESSION_KEY = (
        SELECT GAME_SESSION_KEY FROM GAME_SESSION
        WHERE PLAYER_KEY = 1
        ORDER BY GAME_SESSION_KEY DESC
        FETCH FIRST ROW ONLY
    )
    AND N.NCAT_KEY = NC.NCT_KEY
ORDER BY NC.NCT_KEY;

임의의 플레이어 (여기서는 1)의 가장 최근 게임 세션에서 발생한 뉴스들과 
해당 뉴스의 카탈로그 정보를 조회하는 쿼리



-- 손님 pk -> 손님 선호하는 Category 진열장에 있는 선호 Item들
SELECT *
FROM CUSTOMER_CATALOG C, GAME_SESSION_ITEM_DISPLAY D, EXISTING_ITEM I, ITEM_CATALOG IC
WHERE
    C.CUSTOMER_KEY = 1
    AND D.GAME_SESSION_KEY = (
        SELECT GAME_SESSION_KEY FROM GAME_SESSION
        WHERE PLAYER_KEY = 1
        ORDER BY GAME_SESSION_KEY DESC
        FETCH FIRST ROW ONLY
    )
    AND D.ITEM_KEY = I.ITEM_KEY
    AND I.ITEM_CATALOG_KEY = IC.ITEM_CATALOG_KEY
    AND IC.CATEGORY_KEY = C.CATEGORY_KEY
ORDER BY D.DISPLAY_POS;

임의의 손님 (여기서는 1)번이 선호하는 카테고리에 속한 아이템들 중, 
임의의 플레이어 (여기서는 1)의 가장 최근 게임 세션 진열장에 놓인 아이템들을 진열 순서대로 조회하는 쿼리



-- 플레이어의 거래 기록 (Type 4)
SELECT * FROM DEAL_RECORD
WHERE GAME_SESSION_KEY = (
    SELECT GAME_SESSION_KEY FROM GAME_SESSION
    WHERE PLAYER_KEY = 1
    ORDER BY GAME_SESSION_KEY DESC
    FETCH FIRST ROW ONLY
);

임의의 플레이어 (여기서는 1) 가장 최근 게임 세션에서 
발생한 모든 거래 기록(DEAL_RECORD)을 조회하는 쿼리



-- 손님의 정보 + 힌트: 사기정도, 잘수집정도, 부주의함
SELECT CUSTOMER_NAME, IMG_ID, FRAUD, WELL_COLLECT, CLUMSY FROM CUSTOMER_CATALOG WHERE CUSTOMER_KEY = 1;

임의의 플레이어 (여기서는 1)의 이름, 이미지, 사기 성향(FRAUD), 
수집 성향(WELL_COLLECT), 부주의 성향(CLUMSY) 정보를 조회하는 쿼리



-- 거래에 필요한 정보 (레전더리 확률값, 유니크 확률값, 레어 확률값, 진품 확률값) (Type 7)
SELECT
    (10 * CLUMSY) FLAW_BASE,
    (15 + (65 * WELL_COLLECT)) LEGENDARY_P,
    (20 + PROBABILITY_BASE) UNIQUE_P,
    (30 + PROBABILITY_BASE) RARE_P,
    (35 + PROBABILITY_BASE) NORMAL_P,
    FAKE_P,
    (1 - FAKE_P) GENIUE_P
FROM (
    SELECT CC.*, (65 * (1 - WELL_COLLECT) / 3) PROBABILITY_BASE, (10 + 90 * FRAUD) FAKE_P
    FROM CUSTOMER_CATALOG CC WHERE CUSTOMER_KEY = 1
);

임의의 플레이어 (여기서는 1)의 성향(CLUMSY, WELL_COLLECT, FRAUD) 기반으로 
거래에 필요한 아이템 등급 확률과 결함, 위조/진품 확률을 계산하여 조회하는 쿼리



-- 진열장 위치 -> Item
SELECT I.*, IC.*
FROM GAME_SESSION_ITEM_DISPLAY D, EXISTING_ITEM I, ITEM_CATALOG IC
WHERE
    D.DISPLAY_POS = 1
    AND D.GAME_SESSION_KEY = (
        SELECT GAME_SESSION_KEY FROM GAME_SESSION
        WHERE PLAYER_KEY = 1
        ORDER BY GAME_SESSION_KEY DESC
        FETCH FIRST ROW ONLY
    )
    AND D.ITEM_KEY = I.ITEM_KEY
    AND I.ITEM_CATALOG_KEY = IC.ITEM_CATALOG_KEY;

임의의 플레이어 (여기서는 1)의 가장 최근 게임 세션에서 
임의의 진열장 위치 (여기서는 1)에 놓인 아이템과 해당 아이템의 카탈로그 정보를 조회하는 쿼리


-- 다음 날 넘어갈 때, 정산 -> 결과
SELECT
    G.MONEY + SUM(BOUGHT.PURCHASE_PRICE) - SUM(SOLD.SELLING_PRICE) AS TODAY_START,
    G.MONEY AS TODAY_END,
    FLOOR(G.PAWNSHOP_DEBT * 0.05) AS TODAY_INTEREST,
    G.MONEY - FLOOR(G.PAWNSHOP_DEBT * 0.05) AS TODAY_FINAL
FROM ((
    GAME_SESSION G LEFT OUTER JOIN DEAL_RECORD BOUGHT ON
        G.GAME_SESSION_KEY = BOUGHT.GAME_SESSION_KEY
        AND G.DAY_COUNT = BOUGHT.BOUGHT_DATE
    ) LEFT OUTER JOIN DEAL_RECORD SOLD ON
        G.GAME_SESSION_KEY = SOLD.GAME_SESSION_KEY
        AND G.DAY_COUNT = SOLD.SOLD_DATE
    )
WHERE
    G.GAME_SESSION_KEY = (
        SELECT GAME_SESSION_KEY FROM GAME_SESSION
        WHERE PLAYER_KEY = 1
        ORDER BY GAME_SESSION_KEY DESC
        FETCH FIRST ROW ONLY
    )
GROUP BY G.MONEY, G.PAWNSHOP_DEBT;  -- G는 정확히 1개 -> 결과 자체에는 영항 X

임의의 플레이어 (여기서는 1)의 가장 최근 게임 세션에서 하루 거래를 정산하여, 
오늘 시작 자금, 종료 자금, 전당포 이자, 최종 자금을 계산하는 쿼리


-- 다음 주로 넘어갈 때, 정산 (일별 정산 포함) -> 결과
SELECT
    G.MONEY + SUM(BOUGHT.PURCHASE_PRICE) - SUM(SOLD.SELLING_PRICE) AS TODAY_START,
    G.MONEY AS TODAY_END,
    FLOOR(G.PAWNSHOP_DEBT * 0.05) AS TODAY_INTEREST,
    FLOOR(G.PERSONAL_DEBT * 0.0005) AS TODAY_INTEREST_PERSONAL,
    G.MONEY - FLOOR(G.PAWNSHOP_DEBT * 0.05) - FLOOR(G.PERSONAL_DEBT * 0.0005) AS TODAY_FINAL
FROM ((
    GAME_SESSION G LEFT OUTER JOIN DEAL_RECORD BOUGHT ON
        G.GAME_SESSION_KEY = BOUGHT.GAME_SESSION_KEY
        AND G.DAY_COUNT = BOUGHT.BOUGHT_DATE
    ) LEFT OUTER JOIN DEAL_RECORD SOLD ON
        G.GAME_SESSION_KEY = SOLD.GAME_SESSION_KEY
        AND G.DAY_COUNT = SOLD.SOLD_DATE
    )
WHERE
    G.GAME_SESSION_KEY = (
        SELECT GAME_SESSION_KEY FROM GAME_SESSION
        WHERE PLAYER_KEY = 1
        ORDER BY GAME_SESSION_KEY DESC
        FETCH FIRST ROW ONLY
    )
GROUP BY G.MONEY, G.PAWNSHOP_DEBT, G.PERSONAL_DEBT;  -- G는 정확히 1개 -> 결과 자체에는 영항 X

임의의 플레이어 (여기서는 1)의 가장 최근 게임 세션에서 주별 거래를 정산하여, 
오늘 시작 자금, 종료 자금, 전당포 이자, 개인 부채 이자, 최종 자금을 계산하는 쿼리
7일마다 한번씩 정산을 하는데, 매일 전날 대비 정산을 할때는 해당 쿼리의 직전에 있는 쿼리를 사용하고,
7일마다 정산을 할 때는 해당 쿼리를 사용함. 두 쿼리는 비슷하나 완전히 다른 역할을 수행 중.
나의 개인 빚은 이자가 주에 한번만 생기지만, 전당포의 빚은 매일 생기기 때문에, 둘을 구분할 필요가 있다고 판단하였음.


-- 당일 구매한 것들 목록
SELECT BOUGHT.*
FROM GAME_SESSION G, DEAL_RECORD BOUGHT
WHERE
    G.GAME_SESSION_KEY = (
        SELECT GAME_SESSION_KEY FROM GAME_SESSION
        WHERE PLAYER_KEY = 1
        ORDER BY GAME_SESSION_KEY DESC
        FETCH FIRST ROW ONLY
    )
    AND BOUGHT.GAME_SESSION_KEY = G.GAME_SESSION_KEY
    AND BOUGHT.BOUGHT_DATE = G.DAY_COUNT;

임의의 플레이어 (여기서는 1)의 가장 최근 게임 세션에서 
당일 구매한 거래 기록들(BOUGHT) 목록을 조회하는 쿼리


-- 당일 판매한 것들 목록
SELECT SOLD.*
FROM GAME_SESSION G, DEAL_RECORD SOLD
WHERE
    G.GAME_SESSION_KEY = (
        SELECT GAME_SESSION_KEY FROM GAME_SESSION
        WHERE PLAYER_KEY = 1
        ORDER BY GAME_SESSION_KEY DESC
        FETCH FIRST ROW ONLY
    )
    AND SOLD.GAME_SESSION_KEY = G.GAME_SESSION_KEY
    AND SOLD.SOLD_DATE = G.DAY_COUNT;

임의의 플레이어 (여기서는 1)의 가장 최근 게임 세션에서 
당일 판매한 거래 기록들(SOLD) 목록을 조회하는 쿼리



-- 해당 아이디 있는지 확인 (Type 1)
SELECT HASHED_PW FROM PLAYER WHERE PLAYER_ID = 'user001';

임의의 플레이어 ID를 가진(여기서는 PLAYER_ID = 'user001') 플레이어가 존재하는지 확인하고, 
존재하면 해당 계정의 해시된 비밀번호(HASHED_PW)를 조회하는 쿼리



-- 게임 세션(회차) 기록
SELECT G.GAME_END_DAY_COUNT, G.GAME_END_DATE, MGAIN_DEAL.*, MLOSS_DEAL.*
FROM GAME_SESSION G, DEAL_RECORD MGAIN_DEAL, DEAL_RECORD MLOSS_DEAL
WHERE
    G.GAME_SESSION_KEY = (
        SELECT GAME_SESSION_KEY FROM GAME_SESSION
        WHERE PLAYER_KEY = 1
        ORDER BY GAME_SESSION_KEY DESC
        FETCH FIRST ROW ONLY
    )
    AND MGAIN_DEAL.DRC_KEY = (
        SELECT DRC_KEY FROM DEAL_RECORD D
        WHERE D.GAME_SESSION_KEY = G.GAME_SESSION_KEY
        ORDER BY (D.SELLING_PRICE - D.PURCHASE_PRICE) DESC
        FETCH FIRST ROW ONLY
    )
    AND MLOSS_DEAL.DRC_KEY = (
        SELECT DRC_KEY FROM DEAL_RECORD D
        WHERE D.GAME_SESSION_KEY = G.GAME_SESSION_KEY
        ORDER BY (D.SELLING_PRICE - D.PURCHASE_PRICE)
        FETCH FIRST ROW ONLY
    );

임의의 플레이어 (여기서는 1)의 가장 최근 게임 세션에서, 
세션 종료일과 종료 회차 정보와 함께 해당 세션에서 가장 큰 이익을 낸 거래(MGAIN_DEAL)와 
가장 큰 손실을 낸 거래(MLOSS_DEAL)를 조회하는 쿼리



-- 게임 (진행 중, 완료 포함)의 모든 거래 기록: Player 이름과 함께 (Type 2)
SELECT P.PLAYER_ID, D.* FROM PLAYER P, GAME_SESSION G, DEAL_RECORD D
WHERE P.PLAYER_KEY = G.PLAYER_KEY AND G.GAME_SESSION_KEY = D.GAME_SESSION_KEY;

모든 게임 세션(진행 중 및 완료 포함)에서 발생한 거래 기록(DEAL_RECORD)과 
해당 거래를 한 플레이어 이름(PLAYER_ID)을 함께 조회하는 쿼리




-- 게임 (진행 중, 완료 포함)의 일자별 총이익 (판매) 합계: Player 이름과 함께 (Type 3)
SELECT P.PLAYER_ID, G.GAME_SESSION_KEY, SUM(D.PURCHASE_PRICE) FROM (
    ((PLAYER P JOIN GAME_SESSION G ON P.PLAYER_KEY = G.PLAYER_KEY)
        JOIN DEAL_RECORD D ON G.GAME_SESSION_KEY = D.GAME_SESSION_KEY)
) GROUP BY P.PLAYER_ID, G.GAME_SESSION_KEY;

각 플레이어별, 각 게임 세션(GAME_SESSION_KEY)별로 총 구매 금액(PURCHASE_PRICE) 합계를 계산하는 쿼리



-- 회원가입하고, 1번이라도 플레이한 PLAYER (GAME_SESSION이 있는 Player) (Type 5)
SELECT P.PLAYER_ID FROM PLAYER P WHERE EXISTS (SELECT * FROM GAME_SESSION G WHERE P.PLAYER_KEY = G.PLAYER_KEY);

한 번이라도 게임을 플레이한 플레이어 목록을 조회하는 쿼리


-- 5회 이상 플레이한 플레이어들의 ID (Type 6)
SELECT P.PLAYER_ID FROM PLAYER P WHERE P.PLAYER_KEY IN (
    SELECT P.PLAYER_KEY FROM PLAYER P, GAME_SESSION S
    WHERE P.PLAYER_KEY = S.PLAYER_KEY
    GROUP BY P.PLAYER_KEY HAVING COUNT(*) > 5
);

게임 세션을 5회 이상 플레이한 플레이어 목록을 조회하는 쿼리



-- 플레이어별 각 게임 세션별 아이템 개수 (개수 많은 순으로) (Type 9)
SELECT P.PLAYER_ID, G.GAME_SESSION_KEY, COUNT(*)
FROM ((PLAYER P JOIN GAME_SESSION G ON P.PLAYER_KEY = G.PLAYER_KEY)
        JOIN EXISTING_ITEM I ON G.GAME_SESSION_KEY = I.GAME_SESSION_KEY)
GROUP BY P.PLAYER_ID, G.GAME_SESSION_KEY
ORDER BY COUNT(*);

쿼리는 플레이어별, 각 게임 세션에서 가진 아이템 개수를 계산하여 개수가 많은 순으로 정렬하는 쿼리



-- 특정 플레이어가 모든 게임 세션에 걸쳐 발견 못 한 아이템 종류명 (Type 10)
(SELECT IC.ITEM_CATALOG_NAME FROM ITEM_CATALOG IC)
MINUS
(
    SELECT IC.ITEM_CATALOG_NAME FROM GAME_SESSION G, EXISTING_ITEM I, ITEM_CATALOG IC
    WHERE
        G.PLAYER_KEY = 1
        AND G.GAME_SESSION_KEY = I.GAME_SESSION_KEY
        AND I.ITEM_CATALOG_KEY = IC.ITEM_CATALOG_KEY
);

임의의 플레이어 (여기서는 1)이 모든 게임 세션에서 아직 발견하지 못한 아이템 종류명을 조회하는 쿼리
