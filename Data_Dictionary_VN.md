# Giải thích hệ thống Dữ liệu (Data Dictionary)

Vì dữ liệu của hệ thống Predictive Guardians được lấy từ thực tế tại **Ấn Độ** (cụ thể là bang **Karnataka**), có rất nhiều đặc điểm văn hóa, xã hội và pháp lý khác biệt so với Việt Nam.

Tài liệu này giải thích và dịch các thuật ngữ chuyên ngành để giúp bạn hiểu và giải thích dễ dàng hơn khi thuyết trình hoặc làm báo cáo.

---

## 1. Các nhóm tội phạm chính (Crime Categories & Crime Groups)

Các tội phạm trong dữ liệu được chia theo các danh mục lớn (Category) và chi tiết hơn (Crime Group).

### Danh mục tội phạm tổng quát (Crime Categories)
Dịch từ cột `Crime Category`:
- **OTHER OFFENSES**: Các vi phạm khác (không thuộc các nhóm phổ biến bên dưới).
- **TRAFFIC OFFENSES**: Vi phạm giao thông (gây tai nạn, lái xe nguy hiểm...).
- **PUBLIC SAFETY OFFENSES**: Tội phạm xâm phạm an toàn công cộng (gây rối trật tự, bạo loạn, đánh nhau nơi công cộng).
- **MISSING PERSONS AND KIDNAPPING**: Mất tích và Bắt cóc.
- **VIOLENT CRIMES**: Tội phạm bạo lực (hành hung, tấn công, tống tiền bằng bạo lực...).
- **PROPERTY CRIMES**: Tội phạm tài sản (trộm cướp, phá hoại tài sản).
- **CRIMES AGAINST WOMEN**: Tội phạm nhắm vào phụ nữ (quấy rối, bạo hành gia đình, hiếp dâm, tội phạm liên quan đến của hồi môn - Dowry).
- **NEGLIGENCE AND RASH ACTS**: Vi phạm do bất cẩn và thiếu suy nghĩ gây hậu quả.
- **CRIMES AGAINST CHILDREN**: Tội phạm nhắm vào trẻ em (thường liên quan đến đạo luật POCSO - Đạo luật bảo vệ trẻ em khỏi xâm hại tình dục).
- **CYBERCRIME AND FRAUD**: Tội phạm không gian mạng và Lừa đảo.
- **CRIMES AGAINST PUBLIC SERVANTS**: Tội phạm chống người thi hành công vụ.
- **DRUG OFFENSES**: Tội phạm ma túy.
- **INTELLECTUAL PROPERTY OFFENSES**: Tội phạm sở hữu trí tuệ (hàng giả, vi phạm bản quyền).
- **HATE CRIMES**: Tội phạm thù ghét (tấn công vì khác biệt tôn giáo, đẳng cấp, sắc tộc).

### Các nhóm tội phạm chi tiết (Crime Groups)
Một số tội phạm chi tiết thường xuất hiện trong hồ sơ tội phạm:
- **THEFT**: Trộm cắp (lấy lén lút lúc không có người).
- **ROBBERY**: Cướp tài sản (có đe dọa, dùng vũ lực).
- **DACOITY**: Cướp có tổ chức/Băng đảng (luật Ấn Độ định nghĩa *Dacoity* là vụ cướp do nhóm từ 5 người trở lên thực hiện).
- **BURGLARY (DAY/NIGHT)**: Đột nhập, cạy cửa phá khóa vào ban ngày hoặc ban đêm.
- **MURDER / ATTEMPT TO MURDER**: Giết người / Cố ý giết người.
- **CHEATING & FORGERY**: Lừa đảo chiếm đoạt tài sản & Làm giả giấy tờ.
- **CRIMINAL BREACH OF TRUST**: Lạm dụng tín nhiệm chiếm đoạt tài sản.
- **RIOT**: Bạo loạn.

---

## 2. Hiểu về "Tầng lớp/Đẳng cấp" (Cột `Caste`)

Trong bảng dữ liệu `Criminal_Profiling_cleaned.csv` và `Recidivism_cleaned_data.csv`, cột **`Caste`** (Đẳng cấp / Sắc tộc) đóng vai trò cực kỳ quan trọng. 

**a) Hệ thống 5 nhóm truyền thống (Varna System):**
Ở Ấn Độ, xã hội truyền thống được chia thành 4 đẳng cấp chính (Varna) và 1 nhóm nằm ngoài hệ thống này:
1. **Brahmin (Bà La Môn):** Tầng lớp cao nhất (Giáo sĩ, trí thức, học giả). Vị thế xã hội và kinh tế rất cao.
2. **Kshatriya (Sát Đế Lỵ):** Tầng lớp cai trị, chiến binh, tiểu vương.
3. **Vaishya (Phệ Xá):** Tầng lớp thương nhân, chủ trang trại, thợ thủ công bậc cao.
4. **Shudra (Thủ Đà La):** Tầng lớp lao động tay chân, phục vụ cho 3 giai cấp trên. (Hiện nay tầng lớp này và một số nhánh phân tách chiếm số đông và được chính phủ gọi chung là **OBC - Other Backward Classes** hay Giai cấp Cấp thấp khác).
5. **Dalit (Nhóm "Không thể đụng tới" - Untouchables):** Tầng lớp thấp kém nhất, làm các nghề bị coi là "ô uế". Nhóm này cùng với các bộ lạc thiểu số (Adivasi) được chính phủ xếp vào **SC (Scheduled Castes - Giai cấp chịu thiệt thòi)** và **ST (Scheduled Tribes - Bộ lạc chịu thiệt thòi)**. 

*(Lưu ý: Hồi giáo - **Muslim** nằm ngoài hệ thống này nhưng thường được tính như một nhóm nhân khẩu học độc lập).*

**b) Phân tích Top 10 Đẳng cấp phạm tội nhiều nhất trong dữ liệu (Bang Karnataka):**
Dựa vào biểu đồ dữ liệu hồ sơ thực tế của dự án, các cái tên xuất hiện trong Top 10 thuộc về các nhóm chính nào?

1. **ADI KARNATAKA (14.8% - Cao nhất):** Thuộc nhóm **Dalit (SC)**. Ý nghĩa tên gọi là "Những người gốc của Karnataka". Vì bị gạt ra ngoài lề xã hội, nghèo đói và thiếu giáo dục, tỷ lệ dính líu đến tội phạm (thường là trộm cắp mưu sinh hoặc tội phạm bạo lực) của nhóm này luôn ở mức cao nhất.
2. **VOKKALIGA:** Thường được xếp vào **Shudra / OBC**. Mặc dù nguồn gốc là cộng đồng nông dân, nhưng hiện nay họ là một thế lực chính trị và kinh tế rất lớn tại Karnataka (Dominant Caste). Do dân số cực kỳ đông đảo, số lượng vi phạm tuyệt đối tự nhiên sẽ cao (thường liên quan đến bạo lực, tranh chấp đất đai, bạo loạn).
3. **NAYAKA (và nhánh Naik):** Thuộc nhóm **Tribe (ST - Bộ lạc thiểu số)**. Nằm ngoài 4 Varna, đặc điểm kinh tế - xã hội gần giống với Dalit, nên tỷ lệ phạm tội bạo lực/đường phố rất lớn.
4. **ACHARI:** Thuộc nhóm **Shudra / OBC**. Là tập hợp những người làm nghề thủ công (thợ mộc, rèn, thợ kim hoàn). 
5. **Lingayath:** Một tôn giáo/cộng đồng riêng biệt tại Karnataka từng từ chối hệ thống Varna truyền thống, nhưng về mặt xã hội học họ được phân vào nhóm **Dominant Caste / OBC** (Thế lực tương đương Vokkaliga). Dân số đông nên số vụ án cũng cao.
6. **KURUBA:** Thuộc nhóm **Shudra / OBC**. Nghề truyền thống là chăn cừu.
7. **BHOVI:** Thuộc nhóm **Dalit (SC)**. Nghề truyền thống là đào đất, đẽo đá.
8. **MUSLIM:** Nằm ngoài Varna. Chiếm phần lớn dân số vô sản làm nghề tự do tại các thành thị lớn.
9. **GOLLA:** Thuộc nhóm **Shudra / OBC**. Nghề truyền thống là chăn bò (Yadav).

**c) Tỷ lệ phạm tội phản ánh điều gì?**
- **Sự vắng mặt của hệ thống Forward Castes cao cấp:** Các tầng lớp tinh hoa như *Brahmin, Kshatriya, Vaishya* hầu như KHÔNG xuất hiện trong Top 10. Lý do là họ có đặc quyền, học vấn cao, kinh tế ổn định. Nếu có phạm pháp, họ thường dính vào "Tội phạm cổ cồn trắng" (Lừa đảo tài chính, tham nhũng - Cybercrime/Fraud) — hình thức tội phạm có khuynh hướng xảy ra ít vụ án vặt hơn so với trộm cướp đường phố.
- **Tội phạm do Nghèo đói vs. Tội phạm do Dân số đông:** Top 10 phản ánh sự thật khốc liệt của hệ thống phân tầng: Lượng tội phạm cao nhất đến từ nhóm bị đẩy vào đường cùng bần cùng hóa (**Dalit/SC/ST** như Adi Karnataka, Nayaka) và kế đến là những nhóm chiếm phần đông dân số địa phương (**Shudra/OBC** như Vokkaliga, Lingayath).

👉 **Ứng dụng cho bài toán Predictive Guardians:** 
Trong mô hình **Dự đoán tái phạm (Recidivism)** của dự án, thuật toán H2O AutoML đánh trọng số mạnh vào đặc tính `Caste`. Điều này **không đồng nghĩa với phân biệt chủng tộc/giai cấp**, mà là thuật toán đã nội suy được rằng: Thuộc về hệ thống Dalit/ST đồng nghĩa với việc đối tượng có "tỷ lệ thất nghiệp cao, thu nhập thấp, ít cơ hội hoàn lương" dẫn tới chu kỳ tái phạm tội không thể tránh khỏi.

## 3. Đặc điểm Nghề nghiệp (Cột `Occupation` / `Profession`)

Tương tự như tầng lớp/đẳng cấp, **Nghề nghiệp** là một đặc trưng nhân khẩu học phản ánh trực tiếp nguyên nhân gốc rễ và hoàn cảnh phạm tội. Dựa trên biểu đồ "Đối tượng phạm tội làm nghề gì?", ta có thể phân tích Top 10 nghề nghiệp phổ biến nhất trong hồ sơ:

1. **Labourer (Lao động tự do / Làm thuê / Bốc vác)** - *Đứng đầu khối lượng*: Đây là nhóm lao động tay chân không có kỹ năng chuyên môn, thu nhập thấp và bấp bênh nhất (thường trùng khớp với nhóm Dalit hoặc OBC cấp thấp). Sự nghèo khó, thiếu ổn định và môi trường sống phức tạp đẩy nhóm này vào tỷ lệ phạm tội dồi dào nhất (thường là tội trộm cắp mưu sinh, hành hung, gây rối).
2. **Farmer (Nông dân)** - *Thứ 2*: Phản ánh đặc thù của bang Karnataka vẫn lấy nông nghiệp làm trọng tâm ở các vùng ngoại ô và nông thôn. Tội phạm ở nhóm này thường liên quan đến bạo lực cục bộ (tranh chấp đất đai, nguồn nước, ranh giới), thủ tiêu vụ mùa, hoặc bạo lực gia đình truyền thống.
3. **Driver (Tài xế xe tải/chung)** & **Driver-autorickshaw (Tài xế xe ba gác/xe lam)** & **Driver - car (Tài xế ô tô)**: Nhóm tài xế nói chung cộng dồn lại chiếm số lượng cực kỳ lớn. Do đặc thù công việc di chuyển liên tục ngoài đường phố, căng thẳng, cọ xát với đủ loại thành phần xã hội, họ tất yếu hay dính vào các vụ *Traffic Offenses* (Vi phạm giao thông bạo lực, gây hậu quả nghiêm trọng), đụng độ trên đường, hoặc đôi khi bị lợi dụng để vận chuyển hàng cấm.
4. **Businessman (Người buôn bán / Doanh nhân nhỏ)**: Khác với lao động bần cùng, nhóm này thường liên quan đến *Tội phạm kinh tế* (Cheating/Fraud - Lừa đảo, làm giả giấy tờ), tội phạm tài sản hoặc các vụ thuê giang hồ vì tranh chấp hợp đồng, nợ nần kinh doanh.
5. **Factory worker (Công nhân nhà máy)**: Là lực lượng lao động công nghiệp đặc trưng ở Ấn Độ. Nếu phạm tội, thường xoay quanh bạo lực tập thể tại khu công nghiệp, đình công, hoặc trộm cắp vặt do áp lực đời sống.
6. **Hotel employee (Nhân viên khách sạn / Nhà hàng)**: Nhóm lao động dịch vụ cấp thấp, thường dính líu đến các rủi ro tại môi trường làm việc phức tạp hoặc trộm cắp tài sản.
7. **Carpenter (Thợ mộc)**: Nhóm thợ thủ công có nghề tay chân truyền thống (thường mapping trực tiếp với sắc tộc *Achari* ở phần trên). 
8. **Self Employed Others (Tự kinh doanh quy mô nhỏ - Khác)**: Những người kinh doanh lặt vặt trên phố, quán nước vỉa hè, bán lẻ tự phát.

👉 **Mối tương quan Nghề nghiệp - Bối cảnh tội phạm:** 
Sự áp đảo tuyệt đối của nhóm **Labourer** và **Farmer** một lần nữa khẳng định bài toán xã hội học khốc liệt tại đây: **Hành vi phạm tội chủ yếu bắt nguồn từ sức ép sinh tồn và các mâu thuẫn xã hội ở tầng đáy**. 
Trong mô hình học máy (H2O AutoML), khi cột `Occupation = Labourer`, mức độ rủi ro tái phạm (Recidivism) thường được dự đoán tăng lên. Nó báo động cho cảnh sát rằng thay vì chỉ bỏ tù và răn đe, đối tượng lao động nghèo này cần sự hỗ trợ tái hòa nhập xã hội, nếu không, một khi mãn hạn tù, họ sẽ vẫn hoàn không có việc làm và chắc chắn sẽ đi trộm cắp lại.

---

## 4. Hệ thống Địa lý (Districts & Cities)
Dữ liệu của dự án tập trung toàn bộ vào bang **Karnataka**, một tiểu bang rất lớn ở miền Nam Ấn Độ (diện tích bằng khoảng 2/3 diện tích Việt Nam). Thủ phủ của bang này là thành phố **Bengaluru** (trước đây gọi là Bangalore) - được mệnh danh là thung lũng Silicon của Châu Á.

Trong các cột như `District_Name` hoặc `PresentCity` có các địa danh (ví dụ `Bagalkot`, `Ballari`, `Bengaluru City`, `Mysuru City`):
- **Trường hợp thành phố lớn (Đô thị):** Những nơi có từ "City" như `Bengaluru City`, `Mysuru City` là các đại đô thị. Tội phạm ở đây thường là: *Cybercrime (Tội phạm mạng)*, *Traffic Offenses (Giao thông)*, *Property Crimes (Trộm cắp/cướp bóc)*, và tội phạm trí tuệ.
- **Trường hợp vùng huyện/nông thôn:** Những điểm như `Bagalkot`, `Koppal`, `Gadag` chủ yếu là vùng nông thôn hoặc huyện lẻ. Tội phạm ở khu vực này có xu hướng nghiêng về: bạo lực giữa gia đình/làng xã, bạo loạn (`Riot`), giết người (`Murder`), các tội ác chống lại phụ nữ liên quan đến văn hóa/hồi môn, hoặc trộm cắp nông sản.

👉 **Việc làm quen với các tên huyện này giúp bạn:**
Khi trình bày bản đồ phân bổ nguồn lực (Police Resource Allocation) hoặc bản đồ tội phạm (Choropleth), bạn có thể giải thích dễ dàng tại sao `Bengaluru City` yêu cầu nhiều nguồn lực/cảnh sát chuyên trách hơn các vùng khác như `Bagalkot` (đô thị sầm uất, nơi hội tụ người nhập cư so với vùng nông thôn).
