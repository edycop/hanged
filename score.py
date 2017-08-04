"""
does score calculation
"""


class score_accountant(object):
    "does accounting of scores"

    def __init__(self, max_score=210, allowed_attempts=7, callback_func=None):
        self.score = max_score
        self.decrement_ratio = max_score / allowed_attempts
        #self.decrement_ratio = 1
        self.callback_func = callback_func

    def reduce_score(self):
        'reduce score'
        self.score -= self.decrement_ratio
        # if callback function given, return value to callback
        if self.callback_func:
            self.callback_func(self.score)
        else:
            print('[score_console]: new score is {}'.format(self.score))

#==============================================================================
#
#==============================================================================

def normal_test():
    'normal way to use score accountant object'
    # object score calculator is created
    score_count = score_accountant()
    # initial score is 210
    print(score_count.score)
    assert(score_count.score == 210)
    # on player fails, reduce score callback is called
    score_count.reduce_score()
    # program can access to score calculator object actual score
    assert(score_count.score == 180)
    print(score_count.score)

def integrated_object_test():
    'how to integrate accountant object into an app'

    def callback_function(new_score):
        'function that update in the app the new score, ask new score every time'
        print('[score_update]: {}'.format(new_score))

    # object score calculator is created
    score_count = score_accountant(callback_func=callback_function)
    # initial score is 210
    assert(score_count.score == 210)
    # on player fails, reduce score callback is called, looped
    while score_count.score > 10:
        score_count.reduce_score()


if __name__ == '__main__':
    print('start normal test:')
    normal_test()
    print('start integraton test:')
    integrated_object_test()
