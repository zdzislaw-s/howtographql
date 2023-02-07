# howtographql

New line

Commits in this repository record my progress in going through [graphql-python
Tutorial](https://www.howtographql.com/graphql-python/0-introduction/) and
might be helpful to whoever intends to do that tutorial.

Modif: There is a commit that includes Subscriptions, which unfortunately are not
covered in the tutorial.

The commits are roughly aligned with the original chapters (with my take on
naming and such here and there) and are best followed alongside the tutorial.

[`6c12b74`](https://github.com/zdzislaw-s/howtographql/commit/6c12b74abc6ccfcaad1bcec7412ad8a422a5da8f)` Add hackernews/`  
[`a3c193c`](https://github.com/zdzislaw-s/howtographql/commit/a3c193c60d02162a4782f0ce79f0a86b17b433e0)` Configure Graphene Django`  
[`a549683`](https://github.com/zdzislaw-s/howtographql/commit/a549683b58db4a7928bab95fd2efad8afb37ff9a)` Create Links app`  
[`3c20bbe`](https://github.com/zdzislaw-s/howtographql/commit/3c20bbe54ffd42719b8d5a9ccd6f40d972d715c9)` Create first Type and Schema`  
[`4627900`](https://github.com/zdzislaw-s/howtographql/commit/462790064d9aea7d4d5f8a83a054ed2f44df0186)` Introduce GraphiQL`  
[`1de772e`](https://github.com/zdzislaw-s/howtographql/commit/1de772e16782e9b166b94d0c362865eaf8fbdc32)` Mutations`  
[`082f846`](https://github.com/zdzislaw-s/howtographql/commit/082f8461f1a58cdefff9e41fb59e7defe88fbab0)` Create User`  
[`7ecd2f2`](https://github.com/zdzislaw-s/howtographql/commit/7ecd2f203b6427abd83a85888cc3b12eb428560c)` Query Users`  
[`e557a38`](https://github.com/zdzislaw-s/howtographql/commit/e557a38cba03bc9575b0270d091b057b9636cfb0)` Add queries.curl with test queries`  
[`82b651b`](https://github.com/zdzislaw-s/howtographql/commit/82b651b693760937d812176df16303ea4f61e8ea)` User Authentication`  
[`dafefb7`](https://github.com/zdzislaw-s/howtographql/commit/dafefb7b53e9d879a7bd8edd02347beb8aeac829)` Test Authentication`  
[`1602875`](https://github.com/zdzislaw-s/howtographql/commit/16028752c233fc955a5a5ca667cbbd0ae7ef7a93)` Attach Users to Links...`  
[`78458a2`](https://github.com/zdzislaw-s/howtographql/commit/78458a2f3727e42d2a2aeb3539d422e35543f24a)` Add Votes`  
[`b8d6798`](https://github.com/zdzislaw-s/howtographql/commit/b8d679879a2e3a5f1045528f41d9f031348ee6db)` Consolidate schemas into hackernews/schema.py`  
[`84879cf`](https://github.com/zdzislaw-s/howtographql/commit/84879cf9b8b4f9f36db62a1ef1de622f38244624)` Relate Links and Votes`  
[`8b611ca`](https://github.com/zdzislaw-s/howtographql/commit/8b611ca0b4830f0ce7f1dafac5c3970e7a943149)` Rename type names in schema (e.g. s/VoteType/Vote/)`  
[`1a5db7e`](https://github.com/zdzislaw-s/howtographql/commit/1a5db7e74a8ecb70ae3930e2b74b7352e89dabca)` Replace Exception with GraphQLError`  
[`f9a4d26`](https://github.com/zdzislaw-s/howtographql/commit/f9a4d269abd92fe9bd389fc640c34edfdad15540)` Filter Links`  
[`8d8a278`](https://github.com/zdzislaw-s/howtographql/commit/8d8a2788d5752bf9e842a70d9da775e5aac2dc54)` Paginate Links`  
[`c447ceb`](https://github.com/zdzislaw-s/howtographql/commit/c447cebf863d750f3c2fb19370d241a9114626fe)` Fix missed s/Vote/VoteModel/`  
[`f5eb9bc`](https://github.com/zdzislaw-s/howtographql/commit/f5eb9bc71c324e94c98d8c1b82e15990638855be)` Add schema.graphql`  
[`5771ecc`](https://github.com/zdzislaw-s/howtographql/commit/5771ecc87228f8f55a3ce57e7499426dfea1c06b)` Add subscriptions`

## schema.graphql

The [`hackernews/schema.graphql`](hackernews/schema.graphql) file was created with the following code:

```python
>>> import hackernews.wsgi
>>> from hackernews.schema import schema
>>> with open("schema.graphql", "w") as fo:
...   fo.write(str(schema))
```
