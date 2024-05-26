import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import string


class Summarizer:
    def __init__(self, lang='english'):
        """
        Initializes an instance of the class by setting the language used for text processing
        and loading the corresponding set of stop words. The natural language toolkit (NLTK)
        is utilized to download and provide the stop words for the specified language.
        These stop words are then stored in a private variable for use in text processing
        tasks such as tokenization and frequency analysis.

        :param lang: The language to use for processing text. Defaults to 'english'. The language
                     should correspond to one for which NLTK can provide stop words.
        :type lang: str
        """
        self.__lang = lang
        self.__stop_words = set(stopwords.words())
        try:
            nltk.download('stopwords')
            self.__stop_words = set(stopwords.words('turkish'))
        except OSError as e:
            print('Could not load stopwords file: {}'.format(e))

    @staticmethod
    def __clean_text(text: str) -> str:
        """
        Cleans a given text by removing all punctuation and converting all letters to lowercase.

        :param text: The text to be cleaned.
        :type text: str
        :return: The cleaned text with no punctuation and all lowercase letters.
        :rtype: str
        """
        clean_text = text.translate(str.maketrans('', '', string.punctuation)).lower()
        return clean_text

    def __word_tokenize(self, text: str) -> list[str]:
        """
        Tokenizes a given string of text into a list of words after cleaning it.
        The cleaning process involves removing punctuation and converting all letters to lowercase.

        :param text: The text to be tokenized.
        :type text: str
        :return: A list of words from the given text, after cleaning and tokenizing.
        :rtype: list[str]
        """
        clean_text = self.__clean_text(text)
        words = word_tokenize(clean_text)
        return words

    def __create_word_freq_dict(self, text: str) -> dict[str, int]:
        """
        Creates a frequency dictionary for words in the given text.
        The text is first tokenized into words using the __word_tokenize method.
        Each word is then converted to lowercase and checked against a list of stop words
        (assumed to be stored in self.__stop_words). Words that are not in the stop words list
        are counted for their frequency in the text.

        :param text: The text to be analyzed for word frequency.
        :type text: str
        :return: A dictionary where keys are words and values are the corresponding frequencies of these words in the text.
        :rtype: dict
        """
        word_freq_dict = {}
        words = self.__word_tokenize(text)
        for word in words:
            word = word.lower()  # Ensure uniform case for counting
            if word not in self.__stop_words:  # Filter out stop words
                if word in word_freq_dict:
                    word_freq_dict[word] += 1  # Increment count for existing word
                else:
                    word_freq_dict[word] = 1  # Initialize count for new word
        return word_freq_dict

    @staticmethod
    def __sentence_tokenize(text: str) -> list[str]:
        """
        Tokenizes a given string of text into a list of sentences. This method utilizes
        the sent_tokenize function (which should be imported from a relevant library,
        typically NLTK or a similar text processing library) to identify sentence boundaries
        and split the text accordingly.

        :param text: The text to be split into sentences.
        :type text: str
        :return: A list containing the individual sentences from the given text.
        :rtype: list[str]
        """
        sentence = sent_tokenize(text)
        return sentence

    def __create_sentence_freq_dict(self, text: str) -> dict[str, int]:
        """
        Creates a frequency dictionary mapping each sentence in the given text to the total frequency of its words.
        The method first tokenizes the text into sentences using the __sentence_tokenize method.
        It then creates a word frequency dictionary for the entire text using the __create_word_freq_dict method.
        For each sentence, the method calculates the total frequency of all words within that sentence,
        based on their frequencies in the text.

        :param text: The text to be analyzed for sentence frequencies.
        :type text: str
        :return: A dictionary where keys are sentences from the text and values are the total frequencies of their words.
        :rtype: dict
        """
        sentence_freq_dict = {}
        sentences = self.__sentence_tokenize(text)  # Tokenize text into sentences
        word_freq_dict = self.__create_word_freq_dict(text)  # Create a word frequency dictionary for the text
        for sentence in sentences:
            sentence = sentence.lower()  # Convert sentence to lowercase to match word frequencies
            sentence_freq = 0  # Initialize sentence frequency
            for word, freq in word_freq_dict.items():
                if word in sentence:
                    sentence_freq += freq  # Add word's frequency to sentence's total frequency
            sentence_freq_dict[sentence] = sentence_freq
        return sentence_freq_dict

    def __get_average(self, text: str) -> float:
        """
        Calculates the average frequency of words across all sentences in the provided text.
        This method first generates a sentence frequency dictionary using the
        __create_sentence_freq_dict method, where each sentence is mapped to the total frequency
        of its words. It then calculates the average by summing these total frequencies and
        dividing by the number of sentences.

        :param text: The text to be analyzed for the average word frequency per sentence.
        :type text: str
        :return: The average frequency of words across all sentences in the text.
        :rtype: float
        """
        sum_values = 0
        sentence_freq_dict = self.__create_sentence_freq_dict(text)  # Generate sentence frequency dictionary
        for sentence in sentence_freq_dict:
            sum_values += sentence_freq_dict[sentence]  # Sum total frequencies of all sentences
        average = sum_values / len(sentence_freq_dict)  # Calculate average frequency
        return average

    def summarize(self, text: str) -> str:
        summary = ""
        sentences = self.__sentence_tokenize(text)  # Tokenize text into sentences
        sentence_freq_dict = self.__create_sentence_freq_dict(text)  # Create a frequency dictionary for sentences
        average = self.__get_average(text)  # Calculate average frequency of words per sentence
        for sentence in sentences:
            # Add sentence to summary if its frequency is significantly higher than the average
            if (sentence.lower() in sentence_freq_dict) and (sentence_freq_dict[sentence.lower()] > (1.2 * average)):
                summary += " " + sentence
        return summary


if __name__ == "__main__":

    summ = Summarizer("turkish-english-summarizer")

    text = '''Bu projenin yöntemi, mevcut teknolojilerin ve literatürün kapsamlı bir incelemesini içerir. İlk olarak, AI ve NLP teknolojileri ile kütüphane yönetimi ve kitap önerileri alanlarındaki en son gelişmeleri inceleyerek mevcut en iyi uygulamalar anlaşılacaktır. Ardından, bu teknolojileri kullanarak LibrAI uygulaması geliştirilecektir.
    LibrAI uygulamasının geliştirilmesi, C#, ASP.Net Core, MSSQL ve Python gibi teknolojileri içerecek ve NLP algoritmalarını kullanarak kullanıcıların okuma tercihlerini analiz etmek için entegre edilecektir. ASP.Net Core uygulama geliştirme platformu, C# programlama dilini kullanarak fazla miktarda veriyle bile yüksek performansta çalışabilmektedir. Bu nedenle LibrAI web uygulamasının temel yapısını oluşturmak için ASP.Net Core platformu kullanılacaktır. Çok fazla çeşitli fonksiyon içerek bu temel yapı oluşturulurken katmanlı yapısı sayesinde projenin daha kolay yönetilmesine, denetlenmesine, test edilmesine ve geliştirilmesine olanak tanıyan Model View Controller (MVC) mimari modeli kullanılacaktır. Kitap verilerini ve kullanıcı bilgilerini depolamak için Microsoft şirketi tarafından geliştirilen Microsoft SQL (MSSQL), yine Microsoft firmasına ait olan ASP.Net Core ile en uyumlu biçimde entegre edilebilen ve çalışan veri tabanı olduğu için kullanılacaktır. Python, doğal dil işleme (NLP) algoritmalarını entegre etmek için kullanılacaktır. Kütüphane yönetimi için kullanılacak araçlar ve işlemler, kütüphane yöneticilerinin koleksiyonları daha etkin bir şekilde yönetmelerine olanak tanıyacaktır.
    LibrAI uygulamasında kullanılacak olan yapay zekâ tabanlı kişiselleştirilmiş öneri motorunun geliştirilmesi için 4 aşamalı bir model geliştirme süreci planlanmıştır. Bu model geliştirme süreci; veri toplama ve temizleme, verilerin işlenmesi ve yapay zekâ modelinin eğitilmesi, performans ve hız optimizasyonunun yapılması ve A/B testleri ve iyileştirmelerin yapılması aşamalarını kapsar.
    Veri toplama aşaması için Manisa Celal Bayar Üniversitesi kütüphane yönetimi ile yapılan görüşme ve toplantılar doğrultusunda, kütüphane bünyesinde yer alan 10.000 kitap ve 1.000 kullanıcının son 5 yıl içerisinde ödünç aldığı kitapların verileri tarafımıza iletilecektir. (Projenin desteklenmesi halinde Manisa Celal Bayar Üniversitesi Etik Kurulu'ndan çalışmanın yapılabilmesi için etik kurul onay belgesi alınacaktır.) 10.000 kitap künyesinde yer alan kitabın adı, yazarı, yayın tarihi, türü, alt biçimi, dönemi, dili, konusu ve yayınlayan kuruluş bilgileri veri olarak değerlendirilecektir. 1.000 kullanıcının kütüphane veri tabanındaki ID numarası, kullanıcının kitap ödünç alma geçmişi, kullanıcının favorilere eklediği kitapların verileri kullanılacaktır. Bu veriler MSSQL veri tabanına kaydedilmeden önce gereksiz veriler temizlenerek işlemeye uygun hale getirilecektir.
    Veri toplama aşaması tamamlandıktan sonra, toplanan veriler MSSQL veri tabanına kaydedilecek ve gereksiz veriler temizlenerek işlenmeye uygun hale getirilecektir. Veri setinin hazır hale getirilmesiyle birlikte, yapay zekâ modelinin eğitimine başlanacaktır. Yapay zekâ modelinin eğitimi için “Hybrid Recommendation Algorithm” (Hibrit Öneri Algoritması) tekniği kullanılacaktır. Bu teknik “Collaborative Filtering” (İşbirlikçi Filtreleme) ve “Content-Based Filtering” (İçerik Tabanlı Filtreleme) algoritmalarını içerir. Hibrit yaklaşımlar bazı durumlarda daha etkili olabilir. Bu yöntemler, tavsiye sistemlerindeki “Cold Start” (Soğuk Başlangıç) ve “Sparsity Problem” (Seyreklik Sorunu) gibi bazı yaygın sorunların üstesinden gelmek için de kullanılabilir [2].
    Hibrit yaklaşımların üç stratejisi vardır. Birincisi, “Content-Based Filtering” ve “Collaborative Filtering” algoritmalarını ayrı ayrı uygulamak ve daha sonra bunları birleştirmektir. İkincisi, “Collaborative Filtering” yaklaşımına “Content-Based Filtering” yetenekleri ekleyerek (veya tam tersi), üçüncüsü ise yaklaşımları tek bir modelde birleştirerek [3]. Bu yaklaşımlar projede en doğru ve en etkin modeli geliştirmek üzere denenecektir. “Content-Based Filtering” algoritması kütüphanedeki herhangi iki kitap arasındaki benzerlik oranına bağlı olarak uygulanır. Kitaplar arasındaki benzerlikleri bulmak için kitapları temsil edecek “Embedding” (Metin Gömme) tekniği kullanılacaktır. “Embedding”, sözcüklerin hem anlamsal hem de sözdizimsel bilgilerini yakalar ve NLP görevlerinde yaygın olarak kullanılan kelime benzerliklerini ölçmek için kullanılabilir [4]. Projede önceden eğitilmiş bir “Embedding” modeli kullanılacaktır. Bu modelden istenilen verim alınamadığı takdirde kütüphanedeki kitaplara özgü bir “Embedding” modeli eğitilecektir. Bu model ile metinler gömüldükten sonra iki kitap arasındaki benzerlik oranını belirlemek için bir benzerlik metriği (Cosine benzerliği, Jaccard benzerliği vb.) seçilecektir. Bu adımları sayesinde kitaplar arasındaki metin benzerliği anlaşılmış olacak ve benzer kitaplar kullanıcılara önerilecektir.
    “Content-Based Filtering” algoritma yöntemlerinden farklı olarak, “Collaborative Filtering”, daha önce diğer kullanıcılar tarafından derecelendirilen öğelere dayalı olarak belirli bir kullanıcı için öğelerin faydasını tahmin etmeye çalışır [5]. Kullanıcıların kitapları derecelendirdiği, incelediği, favori olarak işaretlediği ve ödünç aldığı verilerle kullanıcılar arasındaki benzerlikleri belirlemek için bir benzerlik matrisi oluşturulacaktır. Bu matris, her iki kullanıcının geçmiş davranışlarına dayalı olarak kullanıcı benzerliklerini ölçecektir. Bu matrisi oluşturmak için'“Cosine benzerliği veya “Pearson korelasyonu” gibi metriklerden yararlanılacaktır. Belirli bir kullanıcıya öneri yapmak için öneri listesi oluşturulacak ve benzer kullanıcıların beğendiği veya ödünç aldığı kitaplar bu öneri listesine eklenecektir.
    Bu algoritma yöntemleri baz alınarak en doğru model seçimi gerçekleştirilecektir. Bu seçim ardından, modelin performansını ve hızını optimize etmek için gerekli iyileştirmeler yapılacaktır. Modelin etkinliği çeşitli metriklerle değerlendirilecek ve performans artırıcı önlemler alınacaktır. Optimizasyon aşamasının tamamlanmasının ardından, A/B testleri uygulanacak ve modelin kullanıcılar üzerindeki etkisi değerlendirilecektir. Elde edilen sonuçlara göre modelde gerekli görülen iyileştirmeler yapılacak ve sürekli olarak güncellenerek kullanıcı deneyimini artırmaya yönelik çabalara devam edilecektir.
    Bu süreçlerin tamamlanmasıyla LibrAI uygulamasında kullanılacak yapay zekâ tabanlı kişiselleştirilmiş öneri motoru, kullanıcıların kitap seçimlerini optimize etmek ve kütüphane deneyimini zenginleştirmek amacıyla kullanıma hazır hale gelecektir. Araştırmanın ilerleyen aşamalarında, kullanıcıların uygulamayı kullanımı ve geri bildirimleri incelenecek, bu da sürekli iyileştirmeleri ve güncellemeleri yönlendirecektir.'''

    text2 = '''President Vladimir V. Putin on Monday acknowledged for the first time that the bloody assault on a concert hall near Moscow was executed by “radical Islamists,” but he insisted that Ukraine could still have played a role despite the Islamic State’s claim of responsibility.

As Russians grieved, bringing flowers and candles to makeshift memorials across the country, Mr. Putin said that the tragedy was likely ordered by Ukraine,  a statement that shifted attention from his government’s security failure and could also help his war effort.

“The question is: Who benefited from it?” Mr. Putin said, referring to the  worst attack in the capital in two decades, during a publicly broadcast meeting with government officials. “This atrocity can be just an element in a series of attempts of those who have been at war with our country since 2014,” he said, referring to the Ukrainian government.'''
    print(" ORIGINAL TEXT ".center(174, "-"))
    print(text2)

    summary = summ.summarize(text2)

    print(" SUMMARIZED TEXT ".center(174, "-"))
    print(summary)

    print("*"*174)

    print(" ORIGINAL TEXT ".center(174, "-"))
    print(text)

    summary = summ.summarize(text)

    print(" SUMMARIZED TEXT ".center(174, "-"))
    print(summary)
