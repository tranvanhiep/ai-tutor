import warnings
from application import Application
from IPython.display import Markdown

warnings.filterwarnings('ignore')

if __name__ == "__main__":
    inputs = {
        "grade": 7,
        "question": '<div class="question-content__1pw2-"><div class="markup"><div><div><div><div class="_33s8iDB86ShboS4mZ56Q4l"><div class="solution"><p class="kLnDsmZC8c49r2Ntz8LHD"><span>次の減法を加法に直して計算しなさい。</span></p><p class="kLnDsmZC8c49r2Ntz8LHD"><span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mn>0</mn><mo>−</mo><mo stretchy="false">(</mo><mo>+</mo><mn>3</mn><mo stretchy="false">)</mo></mrow><annotation encoding="application/x-tex">0-(+3)</annotation></semantics></math></span></span></span><span></span></p></div><div></div></div></div></div></div><div></div></div></div>',
        "explanation": '<div class="solution-content__1icoL"><div class="markup"><div><div><div><div class="_33s8iDB86ShboS4mZ56Q4l"><div class="solution"><p class="kLnDsmZC8c49r2Ntz8LHD"><span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mtext></mtext><mn>0</mn><mo>−</mo><mo stretchy="false">(</mo><mo>+</mo><mn>3</mn><mo stretchy="false">)</mo></mrow><annotation encoding="application/x-tex">~~~~0-(+3)</annotation></semantics></math></span></span></span><span></span></p><p class="kLnDsmZC8c49r2Ntz8LHD"><span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mo>=</mo><mn>0</mn><mo>+</mo><mo stretchy="false">(</mo><mo>−</mo><mn>3</mn><mo stretchy="false">)</mo></mrow><annotation encoding="application/x-tex">=0+(-3)</annotation></semantics></math></span></span></span><span></span></p><p class="kLnDsmZC8c49r2Ntz8LHD"><span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mo>=</mo><mn>0</mn><mo>−</mo><mn>3</mn></mrow><annotation encoding="application/x-tex">=0-3</annotation></semantics></math></span></span></span><span></span></p><p class="kLnDsmZC8c49r2Ntz8LHD"><span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mo>=</mo><mo>−</mo><mn>3</mn></mrow><annotation encoding="application/x-tex">=-3</annotation></semantics></math></span></span></span><span></span></p></div><div></div></div></div></div></div><div></div></div></div>',
        "result": "-3",
    }
    app = Application()
    app.setup()
    result = app.run(inputs)
    Markdown(result.raw)
