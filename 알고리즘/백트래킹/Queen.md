## Queen

백준에 Queen 문제를 해결하면서 코드를 보면 쉽게 이해할 수 있지만 의문이 드는 부분을 강력하게 짚고자 한다.

가장 빠르게 접근할 수 있는 방법은 방문했는지 혹은 방문하지 않았는지 둘중 하나 인데 여기서 드는 의문은 다음과 같다.

P1. row는 왜 체크 하지 않았을까?

A1. `맵을 그려보면 쉽게 이해할 수 있는데, 퀸의 공격방향은 row, column, 좌대각선, 우대각선 으로 볼 수 있다. 그래서 (row, col)에 이미 배치했다면 해당 row+1 로 갈 수 있으므로 그 행은 검사하지 않는다. `

P2. (0,0) 부터 가도 될까?? 경우의 수는 (0,1) 에도 처음에 배치할 수 있어서 전체 배치 가능한 수가 달라지지 않을까?

A2. `어려운 고민인데, 우선 퀸 의 배치 방법은 달라지지 않는다. 라는 가정이 있어야 할것 같다.`

각 `Point`에 대해 다른 의견이 있으면 공유 부탁드립니다.

```java
import java.util.*;
public class Main {
    static boolean[][] a = new boolean[15][15];
    static int n;
    static boolean[] check_col = new boolean[15];
    static boolean[] check_dig = new boolean[40];
    static boolean[] check_dig2 = new boolean[40];
    static boolean check(int row, int col) {
        // |
        if (check_col[col]) {
            return false;
        }
        // \
        if (check_dig[row+col]) {
            return false;
        }
        // /
        if (check_dig2[row-col+n]) {
            return false;
        }
        return true;
    }
    static int calc(int row) {
        if (row == n) {
            // ans += 1;
            return 1;
        }
        int cnt = 0;
        for (int col=0; col<n; col++) {
            if (check(row, col)) {
                check_dig[row+col] = true;
                check_dig2[row-col+n] = true;
                check_col[col] = true;
                //a[row][col] = true;
                cnt += calc(row+1);
                check_dig[row+col] = false;
                check_dig2[row-col+n] = false;
                check_col[col] = false;
                //a[row][col] = false;
            }
        }
        return cnt;
    }
    public static void main(String args[]) {
        Scanner sc = new Scanner(System.in);
        n = sc.nextInt();
        System.out.println(calc(0));
    }
}
```
