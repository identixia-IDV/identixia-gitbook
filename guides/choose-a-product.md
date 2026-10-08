---
description: Match the GitHub repository to the capability you licensed.
icon: compass
---

# Choose a product

{% hint style="danger" %}
Do not expect liveness in a recognition-only build, or enroll and 1:N search in a liveness-only build.
{% endhint %}

| You need | Face | ID document |
| --- | --- | --- |
| Recognition and liveness | Face Recognition & Liveness Detection | ID Document Recognition & Liveness Detection |
| Recognition only | Face Recognition | ID Document Recognition |
| Liveness only | Face Liveness Detection | ID Document Liveness Detection |

{% columns %}
{% column %}
Full products ship on Android, iOS, Flutter, React Native, Ionic Capacitor, Ionic Cordova, Windows, and Linux / Docker.
{% endcolumn %}
{% column %}
Recognition-only and liveness-only builds exist on a subset of those platforms. [Developers](https://docs.identixia.com/developers) lists the repository for each one.
{% endcolumn %}
{% endcolumns %}

<details>
<summary>SDK Server ports</summary>

| Product | Port |
| --- | --- |
| Document recognition and liveness | 14102 |
| Face recognition and liveness | 14103 |
| Face recognition only | 14104 |
| Face liveness only | 14105 |
| Document recognition only | 14106 |
| Document liveness only | 14107 |

</details>

<a href="https://docs.identixia.com/developers" class="button primary" data-icon="code">Open Developers</a>

{% include "./.gitbook/includes/footer.md" %}
